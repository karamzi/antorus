import hashlib


def generate_signature(amount, currency, order_desc, order_id):
    sting = 'ayvZEvLCS0lAjDfD8LLwry4s282wOWmr|'+amount+'|'+currency+'|1200|1470496|'+order_desc+'|'+order_id+'|https://antorus.com/successOrder/|https://antorus.com/fondyCallback/'
    signature = hashlib.sha1(sting.encode())
    signature = signature.hexdigest()
    return signature
