from django.core.management.base import BaseCommand
from main.models import OrderImages
import datetime


class Command(BaseCommand):
    help = 'clear order images'

    def handle(self, *args, **kwargs):
        date = datetime.datetime.now() - datetime.timedelta(days=60)
        images = OrderImages.objects.filter(date__lte=date)
        for image in images:
            image.delete()
