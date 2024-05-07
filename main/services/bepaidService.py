from typing import Tuple

from main.models import Order
import requests
import json
import base64
from antorus.settings import SITE_HOST, BEPAID_KEY


class BepaidService:
    order: Order
    currency: str

    def __init__(self, order: Order, currency: str):
        self.order = order
        self.currency = currency

    def execute(self) -> Tuple[str, bool]:
        request_object = self._prepare_request()
        auth_token = self._prepare_auth_token()
        success_url, success = self._send_request(request_object, auth_token)
        return success_url, success

    def _prepare_request(self) -> dict:
        request_obj = {
            'checkout': {
                'test': False,
                'transaction_type': 'payment',
                'attempts': 3,
                'settings': {
                    'success_url': f'{SITE_HOST}/successOrder?order_number={self.order.get_order_number()}',
                    'notification_url': f'{SITE_HOST}/bepaidCallback/',
                    'language': 'en'
                },
                'order': {
                    'currency': self.currency,
                    'amount': int(self.order.get_total() * 100),
                    'description': 'payment for order ' + self.order.get_order_number(),
                    'tracking_id': self.order.get_order_number()
                },
                'customer': {
                    'email': self.order.email
                }
            }
        }
        return request_obj

    def _send_request(self, request_obj: dict, auth_token: str) -> Tuple[str, bool]:
        headers = {
            'Authorization': f'Basic ' + auth_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-API-Version': '2'
        }
        response = requests.post('https://checkout.bepaid.tech/ctp/api/checkouts', json=request_obj, headers=headers)
        response_data = json.loads(response.text)
        if response_data.get('errors', False):
            return '', False
        success_url = response_data['checkout']['redirect_url']
        return success_url, True

    @staticmethod
    def _prepare_auth_token() -> str:
        shop_id = 1031
        token = f'{shop_id}:{BEPAID_KEY}'
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return token
