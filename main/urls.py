from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('category/<slug:category>/<slug:subcategory>/', views.subcategory, name='subcategory'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
