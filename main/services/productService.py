from django.db.models import Min
import re


class ProductService:
    @staticmethod
    def get_min_price(product, region):
        from main.models import Products
        currency = 'dollar' if region == 'us' else 'euro'
        if getattr(product, f'price_{currency}', 0):
            return getattr(product, f'price_{currency}', 0)
        else:
            price_min = getattr(product, f'price_{currency}_min', 0)
            discount_price_min = getattr(product, f'discount_price_{currency}_min', 0)
            # if min price of required options equals to 0 or None,
            # we are looking for min price of child required options
            if not discount_price_min and not price_min:
                aggregate_dict = {
                    f'child_options_price_{currency}_min': Min(f'product_required_option_child__price_{currency}'),
                    f'discount_child_options_price_{currency}_min':
                        Min(f'product_required_option_child__new_price_{currency}')
                }
                aggregate_result = Products.objects.filter(pk=product.pk).aggregate(**aggregate_dict)
                price_min = aggregate_result[f'child_options_price_{currency}_min']
                discount_price_min = aggregate_result[f'discount_child_options_price_{currency}_min']
            if discount_price_min and discount_price_min < price_min:
                return discount_price_min
            return price_min

    @staticmethod
    def add_seo_html_tag(product):
        description = product.description
        pattern = r'(<a([^<]*)</a>)'
        find = re.findall(pattern, description)
        for index in range(len(find)):
            if 'rel="nofollow"' in find[index][0]:
                continue
            description = description.replace(find[index][0], f'<a rel="nofollow"{find[index][1]}</a>')
        return description
