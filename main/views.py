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
    Transactions, SEO, SpecialOffers
from .forms import RegisterUserForm
from django.db.models import Q, Prefetch
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from datetime import datetime, timedelta
from .utils.email import Email


def global_var(request):
    categories = Categories.objects.prefetch_related('categories_subcategories').filter(archive=False)
    currency = request.COOKIES.get('currency', 'us')
    path = request.path
    try:
        seo = SEO.objects.get(url=path)
    except ObjectDoesNotExist:
        seo = False
    return {
        'currency': currency,
        'seo': seo,
        'categories': categories,
    }


def index(request):
    only_options = ['name', 'slug', 'image', 'alt', 'short_description', 'new_price_dollar', 'price_dollar',
                    'new_price_euro', 'price_euro']
    products = BestOffersToday.objects.prefetch_related(Prefetch(
        'product',
        queryset=Products.objects.annotate(**Products.annotate_dict).only(*only_options),
    )).all()
    special_offers = SpecialOffers.objects.select_related('product').all()
    context = {
        'products': products,
        'special_offers': special_offers,
    }
    return render(request, 'index.html', context)


def search_products(request):
    if request.method == 'POST':
        products = Products.objects.annotate(**Products.annotate_dict).filter(name__icontains=request.POST['value'],
                                                                              draft=False, archive=False,
                                                                              specialoffers__isnull=True)[:10]
        context = {
            'products': products,
            'search_value': request.POST['value']
        }
        return render(request, 'search_accordion.html', context)
    return redirect(reverse('index'))


def search_result(request, search):
    only_options = ['name', 'slug', 'image', 'alt', 'short_description', 'new_price_dollar', 'price_dollar',
                    'new_price_euro', 'price_euro']
    filter_options = {
        'draft': False,
        'archive': False,
        'specialoffers__isnull': True,
    }
    if search == 'all':
        products = Products.objects.annotate(**Products.annotate_dict).only(*only_options).filter(**filter_options)
    else:
        filter_options['name__icontains'] = search
        products = Products.objects.annotate(**Products.annotate_dict).only(*only_options).filter(**filter_options)
    context = {
        'products': products,
        'search': search,
    }
    return render(request, 'search_result.html', context)


def product(request, slug):
    currency = request.COOKIES.get('currency', 'us')
    try:
        prefetch_options = ['category', 'subcategory', 'product_required_option', 'product_addition_option',
                            'product_required_option__required_option_child__product']
        product = Products.objects.prefetch_related(*prefetch_options).get(slug=slug)
        if product.draft and not request.user.is_superuser:
            return redirect(reverse('index'))
        products = product.category.products_category.annotate(
            **Products.annotate_dict).filter(archive=False, draft=False, specialoffers__isnull=True)[:4]
        context = {
            'product': product,
            'products': products,
        }
        if currency == 'us':
            return render(request, 'product_us.html', context)
        if currency == 'eu':
            return render(request, 'product_eu.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('index'))


def category(request, slug):
    try:
        category = Categories.objects.get(slug=slug)
        products = category.products_category.annotate(
            **Products.annotate_dict).filter(draft=False, archive=False, specialoffers__isnull=True)
        context = {
            'category': category,
            'products': products
        }
        return render(request, 'category.html', context)
    except ObjectDoesNotExist:
        return redirect(reverse('index'))


def subcategory(request, category, subcategory):
    try:
        sub_category = SubCategories.objects.get(slug=subcategory)
        category = Categories.objects.get(slug=category)
        products = sub_category.products_subcategory.annotate(
            **Products.annotate_dict).filter(draft=False, specialoffers__isnull=True)
        context = {
            'category': category,
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
    cart_us = request.COOKIES.get('cartUs', '[]')
    cart_eu = request.COOKIES.get('cartEu', '[]')
    currency = request.COOKIES.get('currency', 'us')
    if currency == 'us' and cart_us == '[]':
        return redirect(reverse('cart'))
    if currency == 'eu' and cart_eu == '[]':
        return redirect(reverse('cart'))
    return render(request, 'checkout.html')


def my_account(request):
    return render(request, 'my_account.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms_of_service.html')


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
                messages.error(request, 'the same username already exists')
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
                    messages.error(request, 'passwords don\'t match')
                    return redirect(reverse('account_details'))
            else:
                messages.error(request, 'incorrect password')
                return redirect(reverse('account_details'))
        user.save()
        messages.success(request, 'details have been updated')
    return redirect(reverse('account_details'))


@login_required(login_url='/myAccount/')
def orders(request):
    orders = Order.objects.filter(user=request.user).exclude(status='3').order_by('-date', '-id')
    context = {
        'orders': orders
    }
    return render(request, 'orders.html', context)


@login_required(login_url='/myAccount/')
def order(request, pk):
    try:
        order = request.user.user_order.get(pk=pk)
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
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            token = {
                'username': username,
                'email': email,
                'password': form.cleaned_data['password1'],
                'time': str(datetime.now()),
            }
            token = json.dumps(token, ensure_ascii=False).encode()
            token = base64.b64encode(token).decode()
            AuthToken.objects.create(token=token)
            url = settings.SITE_HOST + f'/checkEmail/{token}/'
            Email().create_account(email, url, username)
            messages.success(request, f'Confirmation has been sent to {email}')
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
            Email().send_new_password(user, password)
            messages.success(request, f'New password has been sent to {user.email}')
        else:
            messages.error(request, 'the same username or email haven\'t been found')
        return redirect(reverse('reset_password'))
    return redirect(reverse('index'))


def create_order(request):
    if request.method == 'POST':
        sing = '€' if request.POST['currency'] == 'eu' else '$'
        order = Order()
        order.user_id = request.user.pk if request.user.is_authenticated else None
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
            product.price = sing + ' ' + item['price']
            product.total = sing + ' ' + item['total']
            product.order = order
            product.save()
            for item_option in item['options']:
                option = CartOptions()
                option.name = item_option['name']
                option.price = sing + ' ' + item_option['price']
                option.order = order
                option.product = product
                option.save()
        from main.utils.generateSignature import generate_signature
        amount = float(request.POST['total']) * 100
        currency = 'EUR' if request.POST['currency'] == 'eu' else 'USD'
        order_desc = 'payment for order ' + order.get_order_number()
        order_id = order.get_order_number()
        return JsonResponse({
            'status': 'created',
            'amount': str(int(amount)),
            'currency': currency,
            'order_desc': order_desc,
            'order_id': order_id,
            'signature': generate_signature(str(int(amount)), currency, order_desc, order_id),
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
        response = json.dumps(request.POST, ensure_ascii=False)
        order_id = int(request.POST['order_id']) - 1000
        order = Order.objects.get(pk=order_id)
        transaction, status = Transactions.objects.get_or_create(order_id=order_id)
        transaction.order = order
        transaction.service = 1
        transaction.status = request.POST['order_status']
        transaction.currency = request.POST['currency']
        transaction.amount = int(request.POST['amount']) / 100
        transaction.response = response
        date_format = '%d.%m.%Y %H:%M:%S'
        transaction.date = datetime.strptime(request.POST['order_time'], date_format) + timedelta(hours=1)
        transaction.save()
        if request.POST['order_status'] == 'approved':
            Email().send_order(order, 'email/emails.html')
            order.status = 2
        if request.POST['order_status'] == 'declined' or request.POST['order_status'] == 'expired':
            order.status = 3
            Email().send_order(order, 'email/error.html')
        order.save()
        return HttpResponse(status=200)
    return redirect(reverse('index'))


@csrf_exempt
def success_order(request):
    if request.method == 'POST':
        order_id = int(request.POST['order_id']) - 1000
        try:
            order = Order.objects.get(pk=order_id)
            context = {
                'order': order,
            }
            response = render(request, 'success_order.html', context)
            response.delete_cookie('cartUs')
            response.delete_cookie('cartEu')
            response.delete_cookie('coupon')
            return response
        except ObjectDoesNotExist:
            return redirect(reverse('404'))
    return redirect(reverse('index'))
