from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from orders.models import Order
from .models import Transaction
from .services import PaymentService

User = get_user_model()

class TransactionModelTests(TestCase):
    def test_transaction_creation(self):
        tx = Transaction.objects.create(
            order_id='42',
            amount=50000,
            gateway_name='simulated'
        )
        self.assertEqual(tx.status, 'pending')
        self.assertEqual(str(tx), f'Tx {tx.id} - pending')


class PaymentServiceTests(TestCase):
    def setUp(self):
        self.order = Order.objects.create(
            full_name='رضا احمدی',
            phone_number='09121112233',
            address='تهران',
            total_price=50000
        )
        self.service = PaymentService(gateway_name='simulated')

    def test_payment_flow(self):
        # 1. Create transaction
        tx = self.service.create_transaction(order_id=self.order.id, amount=50000)
        self.assertEqual(tx.amount, 50000)
        self.assertEqual(str(tx.order_id), str(self.order.id))

        # 2. Start payment
        url = self.service.start_payment(
            transaction_id=tx.id,
            description='تست پرداخت',
            callback_url='http://testserver/payment/verify/'
        )
        self.assertIsNotNone(url)
        
        tx.refresh_from_db()
        self.assertIsNotNone(tx.transaction_id) # Should have set simulated authority (UUID string)
        
        # 3. Verify payment
        success, verified_tx = self.service.verify_payment(authority=tx.transaction_id, amount=tx.amount)
        self.assertTrue(success)
        self.assertEqual(verified_tx.status, 'success')


class PaymentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.order = Order.objects.create(
            full_name='رضا احمدی',
            phone_number='09121112233',
            address='تهران',
            total_price=50000
        )
        self.tx = Transaction.objects.create(
            order_id=self.order.id,
            amount=50000,
            gateway_name='simulated',
            transaction_id='test-authority'
        )

    def test_request_payment_no_session(self):
        response = self.client.get(reverse('payment:request'))
        self.assertRedirects(response, reverse('core:home'))

    def test_request_payment_success(self):
        session = self.client.session
        session['pending_payment_tx_id'] = self.tx.id
        session.save()

        response = self.client.get(reverse('payment:request'))
        # Should redirect to simulated gateway URL
        self.assertEqual(response.status_code, 302)
        self.assertIn('simulate', response['Location'])

    def test_verify_payment_success(self):
        response = self.client.get(reverse('payment:verify'), {
            'Authority': 'test-authority',
            'Status': 'OK'
        })
        self.assertRedirects(response, reverse('payment:result'))
        
        self.tx.refresh_from_db()
        self.assertEqual(self.tx.status, 'success')
        
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')

    def test_verify_payment_failure(self):
        response = self.client.get(reverse('payment:verify'), {
            'Authority': 'test-authority',
            'Status': 'NOK',
            'Error': 'insufficient_funds'
        })
        self.assertRedirects(response, reverse('payment:result'))
        
        self.tx.refresh_from_db()
        self.assertEqual(self.tx.status, 'failed')
        self.assertEqual(self.tx.callback_data['error'], 'insufficient_funds')

    def test_payment_result_no_session(self):
        response = self.client.get(reverse('payment:result'))
        self.assertRedirects(response, reverse('core:home'))

    def test_payment_result_success(self):
        session = self.client.session
        session['result_tx_id'] = self.tx.id
        session.save()

        response = self.client.get(reverse('payment:result'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment_result.html')
        self.assertEqual(response.context['transaction'], self.tx)
        self.assertEqual(response.context['order'], self.order)

    def test_simulate_payment(self):
        response = self.client.get(reverse('payment:simulate'), {
            'authority': 'test-auth',
            'amount': '50000',
            'callback': 'http://localhost/callback'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/simulate_gateway.html')
