import hashlib


def generate_signature(amount, currency, order_desc, order_id):
    sting = 'ayvZEvLCS0lAjDfD8LLwry4s282wOWmr|'+amount+'|'+currency+'|600|1470496|'+order_desc+'|'+order_id+'|http://151.248.114.152/|http://151.248.114.152/fondyCallback/'
    signature = hashlib.sha1(sting.encode())
    signature = signature.hexdigest()
    return signature
