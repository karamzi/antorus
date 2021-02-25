from django.db import models
from datetime import datetime
from os.path import splitext
from django.shortcuts import reverse


def get_img_path(instance, filename):
    return 'images/%s_%s%s' % (instance.slug, datetime.now().timestamp(), splitext(filename)[1])


class Categories(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории', unique=True)
    slug = models.SlugField(verbose_name='Слаг', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        slug = self.name.strip()
        slug = slug.lower()
        slug = slug.replace(' ', '-')
        self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategories(models.Model):
    category = models.ForeignKey(Categories, related_name='categories_subcategories', verbose_name='Категория',
                                 on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name='Название подкатегории', unique=True)
    slug = models.SlugField(verbose_name='Слаг')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.name.strip()
        slug = slug.lower()
        slug = slug.replace(' ', '-')
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('subcategory', kwargs={'category': self.category.slug, 'subcategory': self.slug})

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Products(models.Model):
    category = models.ForeignKey(Categories, related_name='products_category', verbose_name='Категория',
                                 on_delete=models.PROTECT)
    subcategory = models.ForeignKey(SubCategories, related_name='products_subcategory', blank=True, null=True,
                                    verbose_name='Подкатегория', on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name='Название товара', unique=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to=get_img_path)
    slug = models.SlugField(verbose_name='Слаг')
    length = models.CharField(max_length=255, verbose_name='Длительность')
    char_req = models.CharField(max_length=255, verbose_name='Требования')
    price_dollar = models.IntegerField(default=0, verbose_name='Цена в долларах')
    price_euro = models.IntegerField(default=0, verbose_name='Цена в евро')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.name.strip()
        slug = slug.lower()
        slug = slug.replace(' ', '-')
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class RequiredOption(models.Model):
    product = models.ForeignKey(Products, related_name='product_required_option', on_delete=models.PROTECT,
                                verbose_name='Товар')
    parent_option = models.ForeignKey('self', related_name='child_options', on_delete=models.PROTECT,
                                      verbose_name='Родительская опция', blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price_dollar = models.IntegerField(default=0, verbose_name='Цена в долларах')
    price_euro = models.IntegerField(default=0, verbose_name='Цена в евро')
    new_price_dollar = models.IntegerField(verbose_name='Новая цена в долларах', blank=True, null=True)
    new_price_euro = models.IntegerField(verbose_name='Новая цена в евро', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Обязательная опция'
        verbose_name_plural = 'Обязательные опции'


class AdditionOptions(models.Model):
    product = models.ForeignKey(Products, related_name='product_addition_option', on_delete=models.PROTECT,
                                verbose_name='Товар')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price_dollar = models.IntegerField(default=0, verbose_name='Цена в долларах')
    price_euro = models.IntegerField(default=0, verbose_name='Цена в евро')
    new_price_dollar = models.IntegerField(verbose_name='Новая цена в долларах', blank=True, null=True)
    new_price_euro = models.IntegerField(verbose_name='Новая цена в евро', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительная опция'
        verbose_name_plural = 'Дополнительные опции'
