from django.http import JsonResponse

from main.models import Order
import hashlib


class FondyService:
    currency: str
    order_id: str
    order_desc: str
    amount: str

    def __init__(self, order: Order, currency: str):
        self.currency = currency
        self.order_id = order.get_order_number()
        self.order_desc = 'payment for order ' + order.get_order_number()
        self.amount = self._get_amount(order)

    def _generate_signature(self) -> str:
        sting = 'ayvZEvLCS0lAjDfD8LLwry4s282wOWmr|' + self.amount + '|' + self.currency + '|1200|1470496|' + self.order_desc + '|' + self.order_id + '|https://antorus.com/successOrder/|https://antorus.com/fondyCallback/'
        signature = hashlib.sha1(sting.encode())
        signature = signature.hexdigest()
        return signature

    def _get_amount(self, order: Order) -> str:
        amount = order.get_total() * 100
        amount = str(int(amount))
        return amount

    def json_response(self) -> JsonResponse:
        signature = self._generate_signature()
        response = {
            'status': 'created',
            'amount': self.amount,
            'currency': self.currency,
            'order_desc': self.order_desc,
            'order_id': self.order_id,
            'signature': signature,
        }
        return JsonResponse(response)
