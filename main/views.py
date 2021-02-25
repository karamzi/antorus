from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def product(request, slug):
    return render(request, 'product.html')


def category(request, slug):
    return render(request, 'category.html')


def cart(request):
    return render(request, 'cart.html')
