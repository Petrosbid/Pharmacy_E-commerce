from .models import Transaction
from .gateways import ZarinpalGateway, SimulatedGateway
from django.conf import settings

class PaymentService:
    def __init__(self, gateway_name=None):
        if not gateway_name:
            gateway_name = getattr(settings, 'DEFAULT_PAYMENT_GATEWAY', 'simulated')
        
        if gateway_name == 'zarinpal':
            self.gateway = ZarinpalGateway(merchant_id=getattr(settings, 'ZARINPAL_MERCHANT_ID', 'YOUR-ID'))
        else:
            self.gateway = SimulatedGateway()
            gateway_name = 'simulated'
            
        self.gateway_name = gateway_name

    def create_transaction(self, order_id, amount):
        return Transaction.objects.create(
            order_id=order_id,
            amount=amount,
            gateway_name=self.gateway_name
        )

    def start_payment(self, transaction_id, description, callback_url, mobile=None, email=None):
        tx = Transaction.objects.get(id=transaction_id)
        result = self.gateway.request_payment(tx.amount, description, callback_url, mobile, email)
        
        if result['success']:
            tx.transaction_id = result['authority']
            tx.save()
            return result['url']
        return None

    def verify_payment(self, authority, amount):
        tx = Transaction.objects.get(transaction_id=authority)
        result = self.gateway.verify_payment(authority, amount)
        
        if result['success']:
            tx.status = 'success'
            tx.callback_data = result
            tx.save()
            return True, tx
        else:
            tx.status = 'failed'
            tx.callback_data = result
            tx.save()
            return False, tx
