from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('product/<slug:slug>/', views.product, name='product'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('cart/', views.cart, name='cart'),
]
