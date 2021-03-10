import hashlib


def generate_signature(amount, currency, order_desc, order_id):
    # TODO ссылка на сайт
    sting = 'ayvZEvLCS0lAjDfD8LLwry4s282wOWmr|'+amount+'|'+currency+'|600|1470496|'+order_desc+'|'+order_id+'|https://antorus.com/|https://antorus.com/fondyCallback/'
    signature = hashlib.sha1(sting.encode())
    signature = signature.hexdigest()
    return signature
