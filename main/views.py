from django.shortcuts import render
from .models import Products, Categories, SubCategories


def global_var(request):
    currency = request.COOKIES.get('currency', 'us')
    return {
        'currency': currency
    }


def index(request):
    categories = Categories.objects.all()
    products = Products.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'index.html', context)


def product(request, slug):
    # TODO Обработать ошибку
    product = Products.objects.get(slug=slug)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def category(request, slug):
    categories = Categories.objects.all()
    # TODO Обработать ошибку
    category = Categories.objects.get(slug=slug)
    products = category.products_category.all()
    context = {
        'categories': categories,
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context)


def subcategory(request, category, subcategory):
    categories = Categories.objects.all()
    # TODO Обработать ошибку
    sub_category = SubCategories.objects.get(slug=subcategory)
    products = sub_category.products_subcategory.all()
    context = {
        'categories': categories,
        'sub_category': sub_category,
        'products': products
    }
    return render(request, 'category.html', context)


def cart(request):
    return render(request, 'cart.html')
