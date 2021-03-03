from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from main.utils.customAuth import CustomAuth
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Products, Categories, SubCategories, Order, Cart, CartOptions, Coupon, BestOffersToday, AuthToken, \
    Fondy
from .forms import RegisterUserForm
from django.core.mail import send_mail
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
import base64
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


def search_products(request):
    if request.method == 'POST':
        products = Products.objects.filter(name__icontains=request.POST['value'])
        context = {
            'products': products,
            'search_value': request.POST['value']
        }
        return render(request, 'search_accordion.html', context)
    return redirect(reverse('index'))


def search_result(request, search):
    if search == 'all':
        products = Products.objects.all()
    else:
        products = Products.objects.filter(name__icontains=search)
    categories = Categories.objects.all()
    context = {
        'categories': categories,
        'products': products,
        'search': search,
    }
    return render(request, 'search_result.html', context)


def product(request, slug):
    try:
        product = Products.objects.get(slug=slug)
        context = {
            'product': product
        }
        return render(request, 'product.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('index'))


def category(request, slug):
    try:
        category = Categories.objects.get(slug=slug)
        categories = Categories.objects.all()
        products = category.products_category.all()
        context = {
            'categories': categories,
            'category': category,
            'products': products
        }
        return render(request, 'category.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('index'))


def subcategory(request, category, subcategory):
    try:
        sub_category = SubCategories.objects.get(slug=subcategory)
        categories = Categories.objects.all()
        products = sub_category.products_subcategory.all()
        context = {
            'categories': categories,
            'sub_category': sub_category,
            'products': products
        }
        return render(request, 'category.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('index'))


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


@login_required(login_url='/myAccount/')
def account_details(request):
    return render(request, 'account_details.html')


@login_required(login_url='/myAccount/')
def change_account_details(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        if user.username != request.POST['username']:
            if not User.objects.filter(username=request.POST['username']).exists():
                user.username = request.POST['username']
            else:
                messages.error(request, 'Пользователь с таким логином существует')
                return redirect(reverse('account_details'))
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if request.POST['currentPassword']:
            if check_password(request.POST['currentPassword'], user.password):
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1 and password2 and password1 == password2:
                    user.set_password(password1)
                    login(request, user)
                else:
                    messages.error(request, 'Пароли не совпадают')
                    return redirect(reverse('account_details'))
            else:
                messages.error(request, 'Неправильный пароль')
                return redirect(reverse('account_details'))
        user.save()
        messages.success(request, 'Данные были обновленны успешно')
    return redirect(reverse('account_details'))


@login_required(login_url='/myAccount/')
def orders(request):
    orders = Order.objects.filter(user=request.user)
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)


def order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
        context = {
            'order': order
        }
        return render(request, 'order.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('account_details'))


def create_account(request):
    from antorus import settings
    if request.method == 'POST':
        form = RegisterUserForm(request)
        if form.is_valid():
            form.save(commit=False)
            token = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
            }
            token = json.dumps(token, ensure_ascii=False).encode()
            token = base64.b64encode(token).decode()
            AuthToken.objects.create(token=token)
            url = settings.SITE_HOST + f'/checkEmail/{token}/'
            send_mail('Регистрация', url, 'federation.bratsk@gmail.com',
                      ['play-wow@yandex.ru'],
                      fail_silently=False)
            messages.success(request, f'На почту {form.cleaned_data["email"]} было высланно писмо подтверждения')
        return redirect(reverse('my_account'))
    return redirect(reverse('index'))


def check_auth_token(request, token):
    try:
        token_obj = AuthToken.objects.get(token=token)
        token = base64.b64decode(token_obj.token).decode()
        token = json.loads(token)
        user = User()
        user.username = token['username']
        user.email = token['email']
        user.set_password(token['password'])
        user.save()
        user = authenticate(request, username=token['username'], password=token['password'])
        if user is not None:
            login(request, user)
            token_obj.delete()
            return redirect(reverse('index'))
    except ObjectDoesNotExist:
        pass
    return redirect(reverse('index'))


def send_new_password(request):
    import random
    import string
    if request.method == 'POST':
        user = User.objects.filter(Q(username=request.POST['username']) | Q(email=request.POST['username']))
        if user.exists():
            user = user[0]
            password_characters = string.ascii_letters + string.digits + string.ascii_uppercase
            password = ''.join(random.choice(password_characters) for i in range(15))
            user.set_password(password)
            user.save()
            send_mail('Регистрация', f'Новый пароль: {password}', 'federation.bratsk@gmail.com', ['play-wow@yandex.ru'],
                      fail_silently=False)
            messages.success(request, f'На почту {user.email} было высланно письмо с новым паролем')
        else:
            messages.error(request, 'Такой пользователь не найден')
        return redirect(reverse('reset_password'))
    return redirect(reverse('index'))


def create_order(request):
    if request.method == 'POST':
        sing = '€' if request.POST['currency'] == 'eu' else '$'
        order = Order()
        order.user_id = request.user.pk if request.user.is_authenticated else None
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


@csrf_exempt
def fondy_callback(request):
    if request.method == 'POST':
        print(request.POST)
        fondy = json.dumps(request.POST, ensure_ascii=False)
        fondy = Fondy.objects.create(response=fondy)
        return HttpResponse(status=200)
    return redirect(reverse('index'))
