class OrderApiError(Exception):
    errors: [dict]

    def __init__(self, errors: [dict]):
        self.errors = errors

    def __str__(self):
        error_message = ''
        for error in self.errors:
            error_message += error['message']
        return error_message


class CommonApiError(Exception):
    message: str

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
