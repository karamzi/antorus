import logging

import requests

import base64
import json

from main.models import Order
from antorus.settings import PAYPAL_APP_SECRET, PAYPAL_CLIENT_ID, PAYPAL_URL


class PaypalService:
    @staticmethod
    def generate_access_token() -> str:
        import logging
        auth = f'{PAYPAL_CLIENT_ID}:{PAYPAL_APP_SECRET}'
        auth = base64.b64encode(auth.encode()).decode('utf-8')

        headers = {
            'Authorization': f'Basic {auth}'
        }

        response = requests.post(f'{PAYPAL_URL}/v1/oauth2/token', data='grant_type=client_credentials', headers=headers)

        logging.getLogger('django').error(f'response: {response.status_code}, {response.text}')

        data = json.loads(response.text)

        return data['access_token']

    def create_order(self, order: Order, currency: str) -> dict:
        access_token = self.generate_access_token()
        url = f'{PAYPAL_URL}/v2/checkout/orders'
        payload = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'amount': {
                        'currency_code': currency,
                        'value': order.get_total()
                    }
                }
            ]
        }

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(url, json=payload, headers=headers)

        return json.loads(response.text)

    def capture_payment(self, order_id) -> dict:
        access_token = self.generate_access_token()
        url = f'{PAYPAL_URL}/v2/checkout/orders/{order_id}/capture'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }

        response = requests.post(url, headers=headers)

        return json.loads(response.text)
