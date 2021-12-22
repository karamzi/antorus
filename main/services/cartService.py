from main.models import Products, RequiredOption, RequiredOptionChild, AdditionOptions
import json


def to_fixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


class CartServices:
    region: str
    currency: str
    product: Products
    sign: str

    def __init__(self, request):
        self.session = request.session
        self.request = request
        self.region = request.COOKIES.get('currency', 'us')
        self.currency = 'dollar' if self.region == 'us' else 'euro'
        self.sign = '$' if self.region == 'us' else '€'
        cart = self.session.get(f'cart_{self.region}')
        if not cart:
            cart = self.session[f'cart_{self.region}'] = {
                'products': [],
                'subtotal': 0,
                'discount': 0,
                'total': 0,
                'coupon': '',
                'sign': self.sign,
            }
        self.cart = cart
        self.count_cart()

    def add(self, product_id, options: [str], quantity):
        self.product = Products.objects.get(pk=int(product_id))
        product_json = {
            'id': self.product.pk,
            'name': self.product.name,
            'url': self.product.get_absolute_url(),
            'quantity': quantity,
            'image': self.product.thumb.url,
            'options': [],
        }
        for option in options:
            if option['type'] == 'RequiredOption':
                option = RequiredOption.objects.get(pk=int(option['optionId']))
            elif option['type'] == 'RequiredOptionChild':
                option = RequiredOptionChild.objects.get(pk=int(option['optionId']))
            elif option['type'] == 'AdditionOptions':
                option = AdditionOptions.objects.get(pk=int(option['optionId']))
            product_json['options'].append({
                'name': option.name,
                'price': getattr(option, f'get_price_{self.currency}')()
            })
        product_json['price'] = self.count_price(product_json)
        product_json['total'] = product_json['price'] * int(quantity)
        for index in range(self.count_products()):
            cart_product = self.cart['products'][index]
            if int(cart_product['id']) == self.product.pk:
                self.cart['products'][index] = product_json
                break
        else:
            self.cart['products'].append(product_json)
        self.count_cart()

    def change_quantity(self, product_id, quantity):
        for index in range(self.count_products()):
            cart_product = self.cart['products'][index]
            if cart_product['id'] == int(product_id):
                cart_product['quantity'] = quantity
                cart_product['total'] = cart_product['price'] * quantity
                self.cart['products'][index] = cart_product
        self.count_cart()

    def remove(self, product_id):
        del_product_index = 0
        for index in range(self.count_products()):
            cart_product = self.cart['products'][index]
            if cart_product['id'] == int(product_id):
                del_product_index = index
        self.cart['products'].pop(del_product_index)
        self.count_cart()

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def count_price(self, product_json) -> float:
        total = 0
        total += getattr(self.product, f'get_price_{self.currency}')()
        for option in product_json['options']:
            total += option['price']
        return float(total)

    def count_products(self) -> int:
        return len(self.session[f'cart_{self.region}']['products'])

    def count_cart(self):
        coupon = self.request.COOKIES.get('coupon', False)
        subtotal = 0
        discount = 0
        for cart_product in self.cart['products']:
            subtotal += float(cart_product['total'])
        if coupon:
            coupon = json.loads(coupon)
            self.cart['coupon'] = coupon['name']
            discount = subtotal * coupon['discount'] / 100
            total = subtotal - discount
        else:
            total = subtotal
            self.cart['coupon'] = ''
        self.cart['subtotal'] = to_fixed(subtotal, 2)
        self.cart['discount'] = to_fixed(discount, 2)
        self.cart['total'] = to_fixed(total, 2)
        self.save()

    def clear(self):
        del self.session['cart_us']
        del self.session['cart_eu']
