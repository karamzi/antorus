from django.http import JsonResponse
from django.shortcuts import redirect, reverse
from main.errors.apiErrors import OrderApiError, CommonApiError


class Process500:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        return self._get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, OrderApiError) or isinstance(exception, CommonApiError):
            return JsonResponse({
                'success': False,
                'message': str(exception)
            })
        # TODO сделать ошибку 500
        return redirect(reverse('404'))
