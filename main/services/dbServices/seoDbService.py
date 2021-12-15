from main.models import SEO
from django.core.exceptions import ObjectDoesNotExist


class SeoDbService:
    @staticmethod
    def find(request):
        try:
            seo = SEO.objects.get(url=request.path)
        except ObjectDoesNotExist:
            seo = False
        return seo
