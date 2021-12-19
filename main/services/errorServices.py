from django.http import JsonResponse


class ErrorServices:

    @staticmethod
    def data_error(errors: [dict]):
        return JsonResponse({
            'status': 'error',
            'errors': errors,
        })
