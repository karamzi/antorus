from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from . import models
import re


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = models.Products
        fields = '__all__'


class RequiredOptionAdmin(admin.TabularInline):
    model = models.RequiredOption
    extra = 1


class RequiredOptionChildAdmin(admin.TabularInline):
    model = models.RequiredOptionChild
    extra = 1

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
    extra = 1


class ProductsAdmin(admin.ModelAdmin):
    inlines = [RequiredOptionAdmin, RequiredOptionChildAdmin, AdditionsOptionAdmin]
    form = ProductAdminForm


class CartAdmin(admin.TabularInline):
    readonly_fields = ('product', 'price', 'quantity', 'total')
    model = models.Cart
    extra = 0


class CartOptionsAdmin(admin.TabularInline):
    readonly_fields = ('product', 'name', 'price')
    model = models.CartOptions
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [CartAdmin, CartOptionsAdmin]


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Coupon)
