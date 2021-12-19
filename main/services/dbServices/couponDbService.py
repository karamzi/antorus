from main.models import Coupon
from django.core.exceptions import ObjectDoesNotExist


class CouponDbService:
    coupon: Coupon

    def __init__(self, name: str):
        self._get_coupon(name)

    def increase_coupon_count(self):
        self.coupon.count = self.coupon.count + 1
        self.coupon.save()

    def _get_coupon(self, name: str):
        try:
            self.coupon = Coupon.objects.get(name=name)
        except ObjectDoesNotExist:
            pass
