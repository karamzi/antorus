from django.db.models import Min


class ProductService:
    @staticmethod
    def get_min_price(product, region):
        from main.models import Products
        currency = 'dollar' if region == 'us' else 'euro'
        if getattr(product, f'price_{currency}'):
            return getattr(product, f'price_{currency}')
        else:
            # this attrs have been added by function annotate.
            price_min = getattr(product, f'price_{currency}_min')
            discount_price_min = getattr(product, f'discount_price_{currency}_min')
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
