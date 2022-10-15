from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.utils.safestring import mark_safe
from main.utils.customAdminFilters import ProductArchiveFilter
import re
import nested_admin

from .utils.email import Email
from . import models


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = models.Products
        fields = '__all__'


class EditablePagesAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorWidget())

    class Meta:
        model = models.EditablePages
        fields = '__all__'


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


class RequiredOptionAdmin(admin.TabularInline):
    model = models.RequiredOption
    extra = 0


class AdditionsOptionAdmin(admin.TabularInline):
    model = models.AdditionOptions
    extra = 0


class OrderImagesAdmin(nested_admin.NestedStackedInline):
    model = models.OrderImages
    extra = 0


class ProductsAdmin(admin.ModelAdmin):
    inlines = [RequiredOptionAdmin, RequiredOptionChildAdmin, AdditionsOptionAdmin]
    form = ProductAdminForm
    list_display = ('name', 'category', 'price_dollar', 'price_euro')
    list_display_links = ('name', 'category', 'price_dollar', 'price_euro')
    list_filter = (ProductArchiveFilter,)
    fieldsets = (
        (None, {
            'fields': (('name', 'slug', 'footer_products'),)
        }),
        ('Категория', {
            'fields': (('category', 'subcategory',),),
            'classes': ('sub_category',),
        }),
        (None, {
            'fields': ('short_description', 'description')
        }),
        ('Изображения', {
            'fields': (('image', 'thumb'),),
            'classes': ('sub_category',),
        }),
        ('Общие требования', {
            'fields': (('length', 'char_req'),),
            'classes': ('sub_category',),
        }),
        ('Цены в долларах', {
            'fields': (('price_dollar', 'new_price_dollar'),),
            'classes': ('sub_category',),
        }),
        ('Цены в евро', {
            'fields': (('price_euro', 'new_price_euro'),),
            'classes': ('sub_category',),
        }),
        ('Настройки опций', {
            'fields': (
                ('max_number_required_options', 'max_number_required_child_options', 'max_number_addition_options',
                 'child_required'),),
            'classes': ('sub_category',),
        }),
        ('Архив/Черновик', {
            'fields': (('archive', 'draft'),),
            'classes': ('sub_category',),
        }),
        ('Порядок лота', {
            'fields': ('product_order',),
            'classes': ('sub_category',),
        }),
        ('Seo', {
            'fields': ('alt',),
            'classes': ('collapse', 'sub_category'),
        }),
    )


class CartOptionsAdmin(nested_admin.NestedStackedInline):
    readonly_fields = ('name', 'price')
    model = models.CartOptions
    extra = 0
    fieldsets = (
        (None, {
            'fields': (('name', 'price'),)
        }),
    )


class CartAdmin(nested_admin.NestedStackedInline):
    readonly_fields = ('product', 'price', 'quantity', 'total')
    model = models.Cart
    inlines = [CartOptionsAdmin]
    extra = 0
    fieldsets = (
        (None, {
            'fields': (('product', 'price', 'quantity', 'total'),)
        }),
    )


class OrderAdmin(nested_admin.NestedModelAdmin):
    inlines = [CartAdmin, OrderImagesAdmin]
    list_display = ('__str__', 'date', 'get_status_html', 'total')
    list_display_links = ('__str__', 'date', 'total')
    readonly_fields = (
        'user', 'connection', 'email', 'comment', 'price', 'coupon',
        'total', 'date')
    list_filter = ('status',)
    search_fields = ('pk',)

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        try:
            search_term = int(search_term)
            search_term = search_term - 1000
        except ValueError:
            return queryset, use_distinct
        queryset = models.Order.objects.filter(pk=search_term)
        return queryset, use_distinct

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


class SEOAdmin(admin.ModelAdmin):
    list_display = ('title', 'url')
    list_display_links = ('title', 'url')


class RedirectAdmin(admin.ModelAdmin):
    list_display = ('redirect_from', 'redirect_to')
    list_display_links = ('redirect_from', 'redirect_to')


class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('url', 'time')
    list_display_links = ('url', 'time')


class MonitoringAdmin(admin.ModelAdmin):
    list_display = ('cpu', 'disc', 'ram', 'date')
    list_display_links = ('cpu', 'disc', 'ram', 'date')


class EditablePagesAdmin(admin.ModelAdmin):
    form = EditablePagesAdminForm
    list_display = ('slag',)
    list_display_links = ('slag',)


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.Coupon, CouponAdmin)
admin.site.register(models.BestOffersToday)
admin.site.register(models.Transactions, TransactionsAdmin)
admin.site.register(models.SEO, SEOAdmin)
admin.site.register(models.SpecialOffers)
admin.site.register(models.RedirectModels, RedirectAdmin)
admin.site.register(models.RequestLogsModel, RequestLogAdmin)
admin.site.register(models.MonitoringModel, MonitoringAdmin)
admin.site.register(models.EditablePages, EditablePagesAdmin)
