from abc import ABC, abstractmethod
import requests
import json

class BaseGateway(ABC):
    @abstractmethod
    def request_payment(self, amount, description, callback_url, mobile=None, email=None):
        pass

    @abstractmethod
    def verify_payment(self, authority, amount):
        pass

class ZarinpalGateway(BaseGateway):
    def __init__(self, merchant_id):
        self.merchant_id = merchant_id
        self.request_url = "https://api.zarinpal.com/pg/v4/payment/request.json"
        self.verify_url = "https://api.zarinpal.com/pg/v4/payment/verify.json"
        self.payment_url = "https://www.zarinpal.com/pg/StartPay/"

    def request_payment(self, amount, description, callback_url, mobile=None, email=None):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "description": description,
            "callback_url": callback_url,
            "metadata": {"mobile": mobile, "email": email}
        }
        response = requests.post(self.request_url, data=json.dumps(data), headers={'content-type': 'application/json'})
        result = response.json()
        if result['data'] and result['data']['authority']:
            return {
                'success': True,
                'url': f"{self.payment_url}{result['data']['authority']}",
                'authority': result['data']['authority']
            }
        return {'success': False, 'errors': result.get('errors')}

    def verify_payment(self, authority, amount):
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
        response = requests.post(self.verify_url, data=json.dumps(data), headers={'content-type': 'application/json'})
        result = response.json()
        if result['data'] and result['data']['code'] in [100, 101]:
            return {
                'success': True,
                'ref_id': result['data']['ref_id'],
                'code': result['data']['code']
            }
        return {'success': False, 'errors': result.get('errors')}

class SimulatedGateway(BaseGateway):
    def request_payment(self, amount, description, callback_url, mobile=None, email=None):
        import uuid
        authority = str(uuid.uuid4())
        # We will use a local URL for the simulation
        from django.urls import reverse
        sim_url = f"{reverse('payment:simulate')}?authority={authority}&amount={amount}&callback={callback_url}"
        return {
            'success': True,
            'url': sim_url,
            'authority': authority
        }

    def verify_payment(self, authority, amount):
        # In simulation, we always succeed if called (the simulation view handles the logic)
        import random
        return {
            'success': True,
            'ref_id': str(random.randint(10000000, 99999999)),
            'code': 100
        }
