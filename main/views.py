from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from main.utils.customAuth import CustomAuth
from django.contrib import messages
from .models import Products, Categories, SubCategories, Order, Cart, CartOptions, Coupon, BestOffersToday
import json


def global_var(request):
    currency = request.COOKIES.get('currency', 'us')
    return {
        'currency': currency
    }


def index(request):
    categories = Categories.objects.all()
    products = BestOffersToday.objects.all()
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


def faq(request):
    return render(request, 'faq.html')


def checkout(request):
    # TODO если корзина пустая закрыть страницу
    return render(request, 'checkout.html')


def my_account(request):
    return render(request, 'my_account.html')


def my_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username.find('@') != -1:
            user = CustomAuth()
            user = user.authenticate(request, username=username, password=password)
        else:
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('index'))
        else:
            messages.error(request, 'Username, email or password is incorrect')
    return redirect(reverse('my_account'))


def my_logout(request):
    logout(request)
    return redirect(reverse('my_account'))


def reset_password(request):
    return render(request, 'reset_password.html')


def account_details(request):
    return render(request, 'account_details.html')


def create_order(request):
    if request.method == 'POST':
        sing = '€' if request.POST['currency'] == 'eu' else '$'
        order = Order()
        order.character_server = request.POST['characterServer']
        order.battle_tag = request.POST['battleTag']
        order.faction = request.POST['faction']
        order.connection = request.POST['connection']
        order.email = request.POST['email']
        order.comment = request.POST['comment']
        order.status = 1
        order.total = sing + ' ' + request.POST['total']
        coupon = request.POST.get('coupon', '')
        old_price = request.POST.get('oldPrice', '')
        if coupon:
            order.coupon = coupon
            coupon = Coupon.objects.get(name=coupon)
            coupon.count = coupon.count + 1
            coupon.save()
        if old_price:
            order.price = sing + ' ' + old_price
        else:
            order.price = order.total
        order.save()
        cart = json.loads(request.POST['cart'])
        for item in cart:
            product = Cart()
            product.product = item['name']
            product.quantity = item['quantity']
            product.price = item['currency'] + ' ' + item['price']
            product.total = item['currency'] + ' ' + item['total']
            product.order = order
            product.save()
            for item_option in item['options']:
                option = CartOptions()
                option.name = item_option['name']
                option.price = item['currency'] + ' ' + item_option['price']
                option.order = order
                option.product = product
                option.save()
        return JsonResponse({
            'status': 'created'
        })
    return redirect(reverse('index'))


def check_coupon(request):
    if request.method == 'POST':
        try:
            coupon = Coupon.objects.get(name=request.POST['coupon'])
            return JsonResponse({
                'status': 'True',
                'discount': coupon.discount,
                'name': coupon.name
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                'status': 'False'
            })
    return redirect(reverse('index'))
