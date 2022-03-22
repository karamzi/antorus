from antorus.settings import terminal_key, SITE_HOST
from django.db import connection
from main.models import Order, Transactions
import pandas as pd
import requests
import json


class TinkofService:
    amount: int
    items: [dict]
    order: Order

    def __init__(self, order: Order):
        self.order = order

    def execute(self) -> str:
        data = self._get_cart_items(order_id=self.order.pk)
        self.items = self._prepare_cart_items(data=data)
        self.amount = self._count_amount(data=data)
        request_data = self._prepare_request()
        response = self._send_request(request_data=request_data)
        self._save_response(response)
        return response['PaymentURL']

    def _save_response(self, response: dict):
        Transactions.objects.create(
            order=self.order,
            service='2',
            status=response['Status'],
            currency='RUB',
            amount=response['Amount'] / 100,
            response=json.dumps(response, ensure_ascii=False)
        )

    def _count_amount(self, data: pd.DataFrame) -> int:
        data = data.loc[:, :'total'].drop_duplicates()
        amount = data['total'].sum()
        return amount

    def _send_request(self, request_data) -> dict:
        request_data = json.dumps(request_data, ensure_ascii=False)
        headers = {'Content-type': 'application/json'}
        response = requests.post('https://securepay.tinkoff.ru/v2/Init', data=request_data, headers=headers)
        response = json.loads(response.text)
        return response

    def _prepare_request(self):
        request_json = {
            'TerminalKey': terminal_key,
            'Amount': int(self.amount),
            'OrderId': self.order.get_order_number(),
            'Language': 'en',
            'NotificationURL': f'{SITE_HOST}/tinkofCallback/',
            'SuccessURL': f'{SITE_HOST}/successOrder?OrderId={self.order.get_order_number()}',
            'Receipt': {
                'Email': 'play-wow@yandex.ru',
                'Taxation': 'osn',
                'Items': self.items
            }
        }
        return request_json

    def _prepare_cart_items(self, data: pd.DataFrame) -> [dict]:
        items = []
        products = data['product'].unique()
        for product in products:
            product_options = data[data['product'] == product]
            item = {
                'Name': product_options.iloc[0]['product'],
                'Price': int(product_options.iloc[0]['product_price']),
                'Quantity': int(product_options.iloc[0]['quantity']),
                'Amount': int(product_options.iloc[0]['total']),
                'Tax': 'none'
            }
            items.append(item)
            for row in product_options.itertuples(index=False):
                if row.name is not None:
                    item = {
                        'Name': row.name,
                        'Price': 0,
                        'Quantity': row.quantity,
                        'Amount': 0,
                        'Tax': 'none'
                    }
                    items.append(item)
        return items

    def _get_cart_items(self, order_id: int) -> pd.DataFrame:
        sql = f"""
            SELECT cart.product,
                   cart.quantity,
                   (currency * cart.product_price * 100)::int AS "product_price",
                   cart.name
            FROM (SELECT t1.product,
                   t1.quantity,
                   CASE split_part(t1.price, ' ', 1)
                       WHEN '$' THEN (SELECT us_currency FROM main_currencymodel)
                       WHEN '€' THEN (SELECT eu_currency FROM main_currencymodel)
                       END AS "currency",
                   regexp_replace(t3.total, '\D','')::float AS "product_price",
                   t2.name
                FROM main_cart t1
                LEFT JOIN main_cartoptions t2 ON t1.order_id = t2.order_id
                LEFT JOIN main_order t3 ON t1.order_id = t3.id
                WHERE t1.order_id = {order_id}) AS cart
        """
        data = pd.read_sql(sql, connection)
        data['total'] = data['product_price'] * data['quantity']
        return data
