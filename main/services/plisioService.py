from main.models import Order
import requests
import json
from antorus.settings import SITE_HOST, PLISIO_KEY


class PlisioService:
    order: Order
    currency: str

    def __init__(self, order: Order, currency: str):
        self.order = order
        self.currency = currency

    def execute(self) -> str:
        request_obj = self._prepare_request()
        success_url = self._send_request(request_obj)
        return success_url

    def _prepare_request(self) -> dict:
        request_obj = {
            'currency': 'BTC',
            'order_name': 'payment for order ' + self.order.get_order_number(),
            'order_number': self.order.get_order_number(),
            'source_currency': self.currency,
            'source_amount': self.order.get_total(),
            'callback_url': f'{SITE_HOST}/pisioCallback/',
            'email': self.order.email,
            'api_key': PLISIO_KEY,
        }
        return request_obj

    def _send_request(self, request_obj: dict) -> str:
        response = requests.get('https://plisio.net/api/v1/invoices/new', params=request_obj)
        response_data = json.loads(response.text)
        success_url = response_data['data']['invoice_url']
        return success_url
