from main.models import RedirectModels
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        try:
            redirect_url = RedirectModels.objects.get(redirect_from=path)
            return redirect(redirect_url.redirect_to, permanent=True)
        except ObjectDoesNotExist:
            response = self.get_response(request)
            return response
