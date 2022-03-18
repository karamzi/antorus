from main.errors.apiErrors import OrderApiError
from main.models import Order, Cart, CartOptions
from main.services.dbServices.couponDbService import CouponDbService
from main.services.cartService import CartServices


class OrderService:
    order: Order
    cart: dict

    def __init__(self, request):
        self.request = request
        self.sing = '€' if request.POST.get('currency', 'us') == 'eu' else '$'
        self.cart = CartServices(request).cart

    def create_order(self) -> Order:
        self._check_required_fields()
        self._order_from_json_to_obj()
        self._check_coupon()
        self.order.save()
        self._create_cart()
        return self.order

    def _check_required_fields(self):
        required_fields = {
            'connection': self.request.POST.get('connection', None),
            'email': self.request.POST.get('email', None),
        }
        errors = []
        for key, value in required_fields.items():
            if value is None:
                errors.append({
                    'message': f'The required field - {key} was not found! '
                })
        if errors:
            raise OrderApiError(errors)

    def _check_coupon(self):
        coupon = self.cart['coupon']
        if coupon:
            self.order.coupon = coupon
            CouponDbService(coupon).increase_coupon_count()
            self.order.price = self.sing + ' ' + self.cart['subtotal']

    def _order_from_json_to_obj(self):
        self.order = Order()
        self.order.user_id = self.request.user.pk if self.request.user.is_authenticated else None
        self.order.connection = self.request.POST['connection']
        self.order.email = self.request.POST['email']
        self.order.comment = self.request.POST.get('comment', '')
        self.order.status = 1
        self.order.total = self.sing + ' ' + self.cart['total']
        self.order.price = self.order.total

    def _create_cart(self):
        for item in self.cart['products']:
            product = Cart()
            product.product = item['name']
            product.quantity = item['quantity']
            product.price = self.sing + ' ' + str(item['price'])
            product.total = self.sing + ' ' + str(item['total'])
            product.order = self.order
            product.save()
            for item_option in item['options']:
                option = CartOptions()
                option.name = item_option['name']
                option.price = self.sing + ' ' + str(item_option['price'])
                option.order = self.order
                option.product = product
                option.save()
