import stripe
from antorus.settings import STRIPE_KEY
from main.models import Order


class StripeService:
    order: Order
    currency: str

    def __init__(self, order, currency):
        stripe.api_key = STRIPE_KEY
        self.order = order
        self.currency = currency.lower()

    def execute(self):
        intent = stripe.PaymentIntent.create(
            amount=int(self.order.get_total() * 100),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
            metadata={'order_number': self.order.get_order_number()}
        )
        return intent
