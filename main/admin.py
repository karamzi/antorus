from django.contrib import admin
from . import models
import re


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


# class AdditionsOptionChildAdmin(admin.TabularInline):
#     model = models.AdditionOptionsChild
#     extra = 1
#
#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         path = request.path
#         if len(re.findall(r'/add/$', path)) > 0:
#             return super().formfield_for_foreignkey(db_field, request, **kwargs)
#         digit = re.findall(r'\d+', path)
#         if db_field.name == 'addition_option':
#             kwargs['queryset'] = models.AdditionOptions.objects.filter(product_id=int(digit[0]))
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


class ProductsAdmin(admin.ModelAdmin):
    inlines = [RequiredOptionAdmin, RequiredOptionChildAdmin, AdditionsOptionAdmin]


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
