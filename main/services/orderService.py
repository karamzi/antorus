import json

from main.models import Order, Cart, CartOptions
from main.services.dbServices.couponDbService import CouponDbService


class OrderService:
    order: Order
    errors: [dict]

    def __init__(self, request):
        self.request = request
        self.sing = '€' if request.POST.get('currency', 'us') == 'eu' else '$'

    def create_order(self) -> Order:
        self._order_from_json_to_obj()
        self._check_coupon()
        self.order.save()
        self._create_cart()
        return self.order

    def check_required_fields(self) -> bool:
        required_fields = {
            'connection': self.request.POST.get('connection', None),
            'email': self.request.POST.get('email', None),
            'total': self.request.POST.get('total', None),
            'cart': self.request.POST.get('cart', None),
        }
        self.errors = []
        for key, value in required_fields.items():
            if value is None:
                self.errors.append({
                    'message': f'The required field - {key} was not found'
                })
        if self.errors:
            return False
        return True

    def _check_coupon(self):
        coupon = self.request.POST.get('coupon', None)
        old_price = self.request.POST.get('oldPrice', None)
        if coupon:
            self.order.coupon = coupon
            CouponDbService(coupon).increase_coupon_count()
        if old_price:
            self.order.price = self.sing + ' ' + old_price

    def _order_from_json_to_obj(self):
        self.order = Order()
        self.order.user_id = self.request.user.pk if self.request.user.is_authenticated else None
        self.order.connection = self.request.POST['connection']
        self.order.email = self.request.POST['email']
        self.order.comment = self.request.POST.get('comment', '')
        self.order.status = 1
        self.order.total = self.sing + ' ' + self.request.POST['total']
        self.order.price = self.order.total

    def _create_cart(self):
        cart_json = json.loads(self.request.POST['cart'])
        for item in cart_json:
            product = Cart()
            product.product = item['name']
            product.quantity = item['quantity']
            product.price = self.sing + ' ' + item['price']
            product.total = self.sing + ' ' + item['total']
            product.order = self.order
            product.save()
            for item_option in item['options']:
                option = CartOptions()
                option.name = item_option['name']
                option.price = self.sing + ' ' + item_option['price']
                option.order = self.order
                option.product = product
                option.save()
