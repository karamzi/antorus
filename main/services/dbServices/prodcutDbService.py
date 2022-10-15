from main.models import Products
from django.db.models import Min


class ProductDbService:
    annotate_dict = {
        'price_dollar_min': Min('product_required_option__price_dollar'),
        'discount_price_dollar_min': Min('product_required_option__new_price_dollar'),
        'price_euro_min': Min('product_required_option__price_euro'),
        'discount_price_euro_min': Min('product_required_option__new_price_euro'),
    }

    @staticmethod
    def get_all_products(include_archive=False):
        only_options = ['name', 'slug', 'image', 'alt', 'short_description', 'new_price_dollar', 'price_dollar',
                        'new_price_euro', 'price_euro']
        default_filter = {
            'draft': False,
            'archive': False,
            'specialoffers__isnull': True,
        }
        if include_archive:
            del default_filter['archive']
        return Products.objects.annotate(**ProductDbService.annotate_dict) \
            .only(*only_options) \
            .filter(**default_filter)

    @staticmethod
    def get_products_by_category(category):
        products = ProductDbService.get_all_products()
        return products.filter(category=category)

    @staticmethod
    def get_products_by_subcategory(subcategory):
        products = ProductDbService.get_all_products(include_archive=True)
        return products.filter(subcategory=subcategory)

    @staticmethod
    def search_filter(value, quantity=10):
        products = ProductDbService.get_all_products()
        return products.filter(name__icontains=value)[:quantity]

    @staticmethod
    def get_product(slug):
        prefetch_options = ['category', 'subcategory', 'product_required_option', 'product_addition_option',
                            'product_required_option__required_option_child__product']
        return Products.objects.prefetch_related(*prefetch_options).get(slug=slug)

    @staticmethod
    def get_footer_products():
        return Products.objects.filter(footer_products=True).only('name', 'slug')
