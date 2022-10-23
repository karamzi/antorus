from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from main.utils.customAuth import CustomAuth
from django.contrib import messages
from django.contrib.auth.models import User

from .errors.apiErrors import CommonApiError
from main.services.plisioService import PlisioService
from .models import Order, BestOffersToday, AuthToken, Transactions, SpecialOffers, EditablePages
from .forms import RegisterUserForm
from django.db.models import Q, Prefetch
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from datetime import datetime, timedelta

from .services.cartService import CartServices
from .services.logRequest import LogRequest
from .services.dbServices.categoriesDbService import CategoriesDbService
from .services.dbServices.couponDbService import CouponDbService
from .services.dbServices.prodcutDbService import ProductDbService
from .services.dbServices.seoDbService import SeoDbService
from .services.orderService import OrderService
from .services.stripeService import StripeService
from .utils.email import Email


def global_var(request):
    currency = request.COOKIES.get('currency', 'us')
    cart_service = CartServices(request)
    categories = CategoriesDbService.get_categories_with_subcategories()
    seo = SeoDbService.find(request)
    footer_products = ProductDbService.get_footer_products()
    return {
        'currency': currency,
        'seo': seo,
        'categories': categories,
        'cart': cart_service.get_cart(),
        'footer_products': footer_products,
    }


def index(request):
    products = BestOffersToday.objects.prefetch_related(Prefetch(
        'product',
        queryset=ProductDbService.get_all_products(),
    )).all()
    special_offers = SpecialOffers.objects.select_related('product').all()
    context = {
        'products': products,
        'special_offers': special_offers,
    }
    return render(request, 'index.html', context)


def search_products(request):
    if request.method == 'POST':
        products = ProductDbService.search_filter(request.POST['value'])
        context = {
            'products': products,
            'search_value': request.POST['value']
        }
        return render(request, 'search_accordion.html', context)
    return redirect(reverse('index'))


def search_result(request, search):
    if search == 'all':
        products = ProductDbService.get_all_products()
    else:
        products = ProductDbService.search_filter(search)
    context = {
        'products': products,
        'search': search,
    }
    return render(request, 'search_result.html', context)


def product(request, slug):
    currency = request.COOKIES.get('currency', 'us')
    product = ProductDbService.get_product(slug)
    if product.draft and not request.user.is_superuser:
        return redirect(reverse('index'))
    else:
        products = ProductDbService.get_products_by_category(product.category)[:4]
        context = {
            'product': product,
            'products': products,
        }
        if currency == 'us':
            return render(request, 'product_us.html', context)
        if currency == 'eu':
            return render(request, 'product_eu.html', context)


def category(request, slug):
    category = CategoriesDbService.get_category(slug)
    products = ProductDbService.get_products_by_category(category)
    context = {
        'category': category,
        'products': products
    }
    return render(request, 'category.html', context)


def subcategory(request, category, subcategory):
    category = CategoriesDbService.get_category(category)
    sub_category = CategoriesDbService.get_subcategory(subcategory)
    products = ProductDbService.get_products_by_subcategory(sub_category)
    context = {
        'category': category,
        'sub_category': sub_category,
        'products': products
    }
    return render(request, 'category.html', context)


def cart(request):
    return render(request, 'cart.html')


def faq(request):
    description = EditablePages.objects.get(slag='faq').description
    context = {
        'description': description
    }
    return render(request, 'faq.html', context)


def checkout(request):
    cart_service = CartServices(request)
    if cart_service.count_products() == 0:
        return redirect(reverse('cart'))
    return render(request, 'checkout.html')


def my_account(request):
    return render(request, 'my_account.html')


def privacy_policy(request):
    description = EditablePages.objects.get(slag='privacyPolicy').description
    context = {
        'description': description
    }
    return render(request, 'privacy_policy.html', context)


def terms_of_service(request):
    description = EditablePages.objects.get(slag='termsOfService').description
    context = {
        'description': description
    }
    return render(request, 'terms_of_service.html', context)


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


def cart_service(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_service = CartServices(request)
        if data['action'] == 'add':
            cart_service.add(data['productId'], data['optionsId'], data['quantity'])
        elif data['action'] == 'change':
            cart_service.change_quantity(data['productId'], data['quantity'])
        elif data['action'] == 'remove':
            cart_service.remove(data['productId'])
        return JsonResponse(cart_service.get_cart())


def create_order(request):
    if request.method == 'POST':
        LogRequest.log(request)
        currency = 'EUR' if request.POST.get('currency', 'us') == 'eu' else 'USD'
        # creating order
        order = OrderService(request).create_order()
        if request.POST['payment_type'] == 'paypal':
            return JsonResponse({
                'success': True,
                'order_number': order.get_order_number()
            })
        elif request.POST['payment_type'] == 'stripe':
            return JsonResponse({
                'success': True,
                'order_number': order.get_order_number()
            })
        else:
            success_url = PlisioService(order=order, currency=currency).execute()
            return JsonResponse({
                'success': True,
                'url': success_url
            })
    return redirect(reverse('index'))


def check_coupon(request):
    if request.method == 'POST':
        coupon_service = CouponDbService(name=request.POST['coupon'])
        coupon = coupon_service.coupon
        if coupon is None:
            raise CommonApiError('Coupon have not been found')
        # update coupon in the cart and get it
        cart_service = CartServices(request)
        cart_service.set_new_coupon(coupon)
        cart = cart_service.get_cart()
        response = JsonResponse({
            'status': True,
            'discount': coupon.discount,
            'name': coupon.name,
            'cart': cart
        })
        response.set_cookie('coupon', coupon.name)
        return response
    return redirect(reverse('index'))


@csrf_exempt
def plisio_calback(request):
    if request.method == 'POST':
        LogRequest.log(request)
        response = json.dumps(request.POST, ensure_ascii=False)
        order_id = int(request.POST['order_number']) - 1000
        order = Order.objects.get(pk=order_id)
        transaction, status = Transactions.objects.get_or_create(order_id=order_id)
        transaction.order = order
        transaction.service = 2
        transaction.status = request.POST['status']
        transaction.currency = request.POST['source_currency']
        transaction.amount = request.POST['source_amount']
        transaction.response = response
        transaction.date = datetime.now() + timedelta(hours=1)
        transaction.save()
        if request.POST['status'] == 'completed':
            Email().send_order(order, 'email/emails.html')
            order.status = '2'
        if request.POST['status'] in ['error', 'expired']:
            order.status = '3'
            Email().send_order(order, 'email/error.html')
        order.save()
        return HttpResponse(status=200)
    return redirect(reverse('index'))


@csrf_exempt
def success_order(request):
    def prepare_order(request, order_id):
        payment_type = request.POST.get('payment_type', None)
        try:
            order = Order.objects.get(pk=order_id)
            order.status = '2'
            order.save()
            context = {
                'order': order,
                'payment_type': payment_type
            }
            response = render(request, 'success_order.html', context)
            cart_service = CartServices(request)
            cart_service.clear()
            response.delete_cookie('coupon')
            return response
        except ObjectDoesNotExist:
            return redirect(reverse('404'))

    if request.method == 'GET':
        LogRequest.log(request)
        order_id = int(request.GET.get('order_number')) - 1000
        return prepare_order(request, order_id)

    if request.method == 'POST':
        LogRequest.log(request)
        order_id = int(request.POST['order_number']) - 1000
        return prepare_order(request, order_id)

    return HttpResponse(status=200)


def stripe(request):
    if request.method == 'POST':
        context = {
            'order_number': request.POST['order_number']
        }
        return render(request, 'stripe.html', context)
    return redirect(reverse('index'))


def stripe_create_payment(request):
    if request.method == 'POST':
        # Create a PaymentIntent with the order amount and currency
        currency = request.COOKIES.get('currency', 'us')
        currency = 'usd' if currency == 'us' else 'eur'
        data = json.loads(request.body)
        order_number = int(data['order_number']) - 1000
        order = Order.objects.get(pk=order_number)
        intent = StripeService(order, currency).execute()
        return JsonResponse({
            'success': True,
            'clientSecret': intent['client_secret']
        })
    return redirect(reverse('index'))
