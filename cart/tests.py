import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from products.models import Category, Product
from .models import Cart, CartItem

User = get_user_model()

class CartModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='دسته ۱', slug='cat-1')
        self.product = Product.objects.create(
            category=self.category,
            name='محصول تستی',
            slug='test-product',
            price=50000,
            quantity=10,
            in_stock=True
        )
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')
        self.cart = Cart.objects.create(user=self.user)
        self.item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_totals(self):
        self.assertEqual(self.cart.total_items, 2)
        self.assertEqual(self.cart.total_price, 100000)
        self.assertEqual(str(self.cart), 'Cart - 09123456789')
        self.assertEqual(str(self.item), '2 x محصول تستی')
        self.assertEqual(self.item.total_price, 100000)

    def test_session_cart_str(self):
        session_cart = Cart.objects.create(session_key='xyz123')
        self.assertEqual(str(session_cart), 'Cart - xyz123')


class CartViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='دسته ۱', slug='cat-1')
        self.product1 = Product.objects.create(
            category=self.category,
            name='محصول ۱',
            slug='prod-1',
            price=30000,
            quantity=5,
            in_stock=True
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name='محصول ۲',
            slug='prod-2',
            price=20000,
            quantity=0,
            in_stock=False  # Out of stock
        )
        self.user = User.objects.create_user(phone_number='09123456789', password='password123')

    def test_cart_detail_view(self):
        # Should work for anonymous users too
        response = self.client.get(reverse('cart:detail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/detail.html')
        self.assertIn('cart', response.context)

    def test_cart_add_success(self):
        # Add to cart
        response = self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 2}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['cart_count'], 2)
        self.assertEqual(data['cart_total'], 60000)

    def test_cart_add_out_of_stock(self):
        response = self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product2.id, 'quantity': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertEqual(data['message'], 'متأسفانه این محصول در حال حاضر موجود نیست')

    def test_cart_add_insufficient_stock(self):
        response = self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 6}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')
        self.assertIn('تعداد درخواستی بیشتر از موجودی انبار است', data['message'])

    def test_cart_update_and_remove(self):
        # First add product
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 2}),
            content_type='application/json'
        )
        # Update quantity (+1)
        response = self.client.post(
            reverse('cart:update'),
            data=json.dumps({'product_id': self.product1.id, 'delta': 1}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 3)

        # Update to <= 0 (should delete)
        response = self.client.post(
            reverse('cart:update'),
            data=json.dumps({'product_id': self.product1.id, 'delta': -3}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 0)

    def test_cart_remove(self):
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 2}),
            content_type='application/json'
        )
        response = self.client.post(
            reverse('cart:remove'),
            data=json.dumps({'product_id': self.product1.id}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 0)

    def test_cart_clear(self):
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 2}),
            content_type='application/json'
        )
        response = self.client.post(reverse('cart:clear'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['cart_count'], 0)

    def test_cart_get_data(self):
        self.client.post(
            reverse('cart:add'),
            data=json.dumps({'product_id': self.product1.id, 'quantity': 2}),
            content_type='application/json'
        )
        response = self.client.get(reverse('cart:data'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['total_items'], 2)
        self.assertEqual(len(data['items']), 1)
        self.assertEqual(data['items'][0]['id'], self.product1.id)
