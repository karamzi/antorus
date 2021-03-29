from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe

from .utils.email import Email
from . import models
import re


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = models.Products
        fields = '__all__'


class RequiredOptionAdmin(admin.TabularInline):
    model = models.RequiredOption
    extra = 0


class RequiredOptionChildAdmin(admin.TabularInline):
    model = models.RequiredOptionChild
    extra = 0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        path = request.path
        if len(re.findall(r'/add/$', path)) > 0:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        digit = re.findall(r'\d+', path)
        if db_field.name == 'required_option':
            kwargs['queryset'] = models.RequiredOption.objects.filter(product_id=int(digit[0]))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class AdditionsOptionAdmin(admin.TabularInline):
    model = models.AdditionOptions
    extra = 0


class OrderImagesAdmin(admin.TabularInline):
    model = models.OrderImages
    extra = 0


class ProductsAdmin(admin.ModelAdmin):
    inlines = [RequiredOptionAdmin, RequiredOptionChildAdmin, AdditionsOptionAdmin]
    form = ProductAdminForm
    list_display = ('name', 'category', 'price_dollar', 'price_euro')
    list_display_links = ('name', 'category', 'price_dollar', 'price_euro')


class CartAdmin(admin.TabularInline):
    readonly_fields = ('product', 'price', 'quantity', 'total')
    model = models.Cart
    extra = 0


class CartOptionsAdmin(admin.TabularInline):
    readonly_fields = ('product', 'name', 'price')
    model = models.CartOptions
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [CartAdmin, CartOptionsAdmin, OrderImagesAdmin]
    list_display = ('__str__', 'date', 'get_status_html', 'total')
    list_display_links = ('__str__', 'date', 'total')
    readonly_fields = (
        'user', 'character_server', 'battle_tag', 'faction', 'connection', 'email', 'comment', 'price', 'coupon',
        'total', 'date')
    list_filter = ('status',)

    def get_status_html(self, obj):
        if obj.status == '1':
            return mark_safe(
                f'<div style="background-color: #e2e3e5; text-align: center; border-radius: 10px; padding: 3px 0;">{obj.get_status_display()}</div>')
        if obj.status == '2':
            return mark_safe(
                f'<div style="background-color: #fff3cd; text-align: center; border-radius: 10px; padding: 3px 0;">{obj.get_status_display()}</div>')
        if obj.status == '3':
            return mark_safe(
                f'<div style="background-color: #f8d7da; text-align: center; border-radius: 10px; padding: 3px 0;">{obj.get_status_display()}</div>')
        if obj.status == '4':
            return mark_safe(
                f'<div style="background-color: #cfe2ff; text-align: center; border-radius: 10px; padding: 3px 0;">{obj.get_status_display()}</div>')
        if obj.status == '5':
            return mark_safe(
                f'<div style="background-color: #badbcc; text-align: center; border-radius: 10px; padding: 3px 0;">{obj.get_status_display()}</div>')

    def save_model(self, request, obj, form, change):
        order = models.Order.objects.get(pk=obj.pk)
        if obj.status == '4' and order != '4':
            Email().send_order(order, 'email/refund.html')
        if obj.status == '5' and order != '5':
            Email().send_order(order, 'email/completed.html')
        super().save_model(request, obj, form, change)

    get_status_html.short_description = 'Статус заказа'


class CouponAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount', 'count')
    list_display_links = ('name', 'discount', 'count')
    readonly_fields = ('count',)


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'service', 'status', 'currency', 'amount', 'date')
    list_display_links = ('__str__', 'service', 'status', 'currency', 'amount', 'date')


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Coupon, CouponAdmin)
admin.site.register(models.BestOffersToday)
admin.site.register(models.Transactions, TransactionsAdmin)
