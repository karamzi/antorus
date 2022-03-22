from django.core.management.base import BaseCommand
from main.models import CurrencyModel

import datetime
import requests
import xml.etree.ElementTree as ET


class Command(BaseCommand):
    help = 'get actual currency from api'

    def handle(self, *args, **options):
        date = datetime.datetime.now()
        date = date.strftime('%d/%m/%Y')
        response = requests.get(f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date}')
        responseXml = ET.fromstring(response.text)
        us_str = responseXml.find('./Valute[@ID="R01235"]').find('Value').text.replace(',', '.')
        eu_str = responseXml.find('./Valute[@ID="R01239"]').find('Value').text.replace(',', '.')
        us = float(us_str)
        eu = float(eu_str)
        obj = CurrencyModel.objects.first()
        obj.us_currency = us
        obj.eu_currency = eu
        obj.save()
