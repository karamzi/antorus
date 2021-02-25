from django.contrib import admin
from . import models


class RequiredOptionAdmin(admin.TabularInline):
    model = models.RequiredOption
    extra = 1


class AdditionsOptionAdmin(admin.TabularInline):
    model = models.AdditionOptions
    extra = 1


class ProductsAdmin(admin.ModelAdmin):
    inlines = [RequiredOptionAdmin, AdditionsOptionAdmin]


admin.site.register(models.Products, ProductsAdmin)
admin.site.register(models.Categories)
admin.site.register(models.SubCategories)
