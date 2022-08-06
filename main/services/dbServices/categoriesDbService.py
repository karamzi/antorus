from main.models import Categories, SubCategories


class CategoriesDbService:
    @staticmethod
    def get_categories_with_subcategories():
        return Categories.objects.prefetch_related('categories_subcategories').filter(archive=False)

    @staticmethod
    def get_category(slug):
        return Categories.objects.get(slug=slug)

    @staticmethod
    def get_subcategory(slug):
        return SubCategories.objects.get(slug=slug)


