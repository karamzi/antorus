from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('category/<slug:category>/<slug:subcategory>/', views.subcategory, name='subcategory'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('createOrder/', views.create_order),
    path('checkCoupon/', views.check_coupon),
    path('faq/', views.faq, name='faq'),
    path('login/', views.login, name='login'),
    path('resetPassword/', views.reset_password, name='reset_password'),
    path('accountDetails/', views.account_details, name='account_details'),
]
