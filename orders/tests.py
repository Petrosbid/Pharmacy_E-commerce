import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Category, Product
from .models import Order, OrderItem
from payment.models import Transaction

User = get_user_model()

class OrderModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='کتگوری ۱', slug='cat-1')
        self.product = Product.objects.create(
            category=self.category,
            name='محصول',
            slug='prod',
            price=20000,
            quantity=5
        )
        self.order = Order.objects.create(
            full_name='رضا احمدی',
            phone_number='09121112233',
            address='تهران، خیابان ولیعصر',
            shipping_method='standard',
            payment_method='cod',
            shipping_cost=0,
            total_price=20000
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=20000
        )

    def test_order_model_str(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} - رضا احمدی')
        self.assertEqual(str(self.item), '1 x محصول')
        self.assertEqual(self.item.get_cost(), 20000)


class OrderViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='کتگوری ۱', slug='cat-1')
        self.product = Product.objects.create(
            category=self.category,
            name='محصول',
            slug='prod',
            price=150000,
            quantity=5
        )
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')

    def test_checkout_get(self):
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

    def test_checkout_post_invalid_json(self):
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'رضا احمدی',
            'phone_number': '09121112233',
            'address': 'تهران',
            'shipping_method': 'standard',
            'payment_method': 'cod',
            'cart_data': 'invalid-json'
        })
        self.assertRedirects(response, reverse('orders:checkout'))

    def test_checkout_post_empty_cart(self):
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'رضا احمدی',
            'phone_number': '09121112233',
            'address': 'تهران',
            'shipping_method': 'standard',
            'payment_method': 'cod',
            'cart_data': '[]'
        })
        self.assertRedirects(response, reverse('products:product_list'))

    def test_checkout_post_success_cod(self):
        cart_data = json.dumps([{'id': self.product.id, 'quantity': 2}])
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'رضا احمدی',
            'phone_number': '09121112233',
            'address': 'تهران',
            'shipping_method': 'express', # express cost = 45000
            'payment_method': 'cod',
            'cart_data': cart_data
        })
        self.assertRedirects(response, reverse('core:home'))
        
        # Verify order and items
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.full_name, 'رضا احمدی')
        self.assertEqual(order.shipping_cost, 45000)
        # 150000 * 2 + 45000 = 345000
        self.assertEqual(order.total_price, 345000)
        
        # Check stock reduction
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 3)

    def test_checkout_post_success_gateway(self):
        cart_data = json.dumps([{'id': self.product.id, 'quantity': 1}])
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'علی علوی',
            'phone_number': '09122223344',
            'address': 'شیراز',
            'shipping_method': 'standard',
            'payment_method': 'gateway',
            'cart_data': cart_data
        })
        # Should redirect to payment:request
        self.assertRedirects(response, reverse('payment:request'), target_status_code=302)
        
        order = Order.objects.first()
        tx = Transaction.objects.first()
        self.assertIsNotNone(tx)
        self.assertEqual(tx.order_id, str(order.id))
        self.assertEqual(self.client.session['pending_payment_tx_id'], tx.id)

    def test_checkout_post_insufficient_stock(self):
        cart_data = json.dumps([{'id': self.product.id, 'quantity': 10}]) # only 5 in stock
        response = self.client.post(reverse('orders:checkout'), {
            'full_name': 'رضا احمدی',
            'phone_number': '09121112233',
            'address': 'تهران',
            'shipping_method': 'standard',
            'payment_method': 'cod',
            'cart_data': cart_data
        })
        self.assertRedirects(response, reverse('cart:detail'))

    def test_tracking_view(self):
        order = Order.objects.create(
            full_name='رضا احمدی',
            phone_number='09121112233',
            address='تهران',
            total_price=50000
        )
        # Valid tracking
        response = self.client.get(reverse('orders:tracking'), {'order_id': order.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], order)

        # Invalid tracking
        response = self.client.get(reverse('orders:tracking'), {'order_id': 9999})
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context['order'])

    def test_order_history_view_unauthenticated(self):
        response = self.client.get(reverse('orders:history'))
        self.assertRedirects(response, f"{reverse('users:login')}?next={reverse('orders:history')}")

    def test_order_history_view_authenticated(self):
        self.client.login(phone_number='09123456789', password='password123')
        order = Order.objects.create(
            user=self.user,
            full_name='تست تاریخچه',
            phone_number='09123456789',
            address='تهران',
            total_price=50000
        )
        response = self.client.get(reverse('orders:history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/history.html')
        self.assertIn(order, response.context['orders'])
