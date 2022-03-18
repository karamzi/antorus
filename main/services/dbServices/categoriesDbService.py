from main.models import Categories, SubCategories
from django.core.exceptions import ObjectDoesNotExist


class CategoriesDbService:
    @staticmethod
    def get_categories_with_subcategories():
        return Categories.objects.prefetch_related('categories_subcategories').filter(archive=False)

    @staticmethod
    def get_category(slug):
        try:
            return Categories.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def get_subcategory(slug):
        try:
            return SubCategories.objects.get(slug=slug)
        except ObjectDoesNotExist:
            return None


