from django.db import models
from datetime import datetime
from os.path import splitext
from django.shortcuts import reverse
from easy_thumbnails.fields import ThumbnailerImageField


def get_img_path(instance, filename):
    return 'images/%s_%s%s' % (instance.slug, datetime.now().timestamp(), splitext(filename)[1])


def get_thumbs_path(instance, filename):
    return 'thumbs/%s_%s%s' % (instance.slug, datetime.now().timestamp(), splitext(filename)[1])


def to_fixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


class Categories(models.Model):
    # TODO Валидация названия
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
    # TODO Валидация названия
    name = models.CharField(max_length=255, verbose_name='Название подкатегории', unique=True)
    slug = models.SlugField(verbose_name='Слаг', blank=True)

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
    # TODO Валидация названия
    name = models.CharField(max_length=255, verbose_name='Название товара', unique=True)
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to=get_img_path)
    thumb = ThumbnailerImageField(upload_to=get_thumbs_path, verbose_name='Миниатюра',
                                  resize_source={'size': (120, 120), 'crop': True})
    slug = models.SlugField(verbose_name='Ссылка', blank=True, null=True)
    length = models.CharField(max_length=255, verbose_name='Длительность')
    char_req = models.CharField(max_length=255, verbose_name='Требования')
    price_dollar = models.DecimalField(verbose_name='Цена в долларах', decimal_places=2, max_digits=5, blank=True,
                                       null=True)
    price_euro = models.DecimalField(verbose_name='Цена в евро', decimal_places=2, max_digits=5, blank=True, null=True)
    quantity_required_options = models.IntegerField(verbose_name='max количество обязательных опций', blank=True,
                                                    null=True)
    quantity_addition_options = models.IntegerField(verbose_name='max количество доп опций', blank=True,
                                                    null=True)
    child_required = models.BooleanField(verbose_name='Дочернии обязательны', default=False)

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
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price_dollar = models.DecimalField(default=0, verbose_name='Цена в долларах', decimal_places=2, max_digits=5)
    price_euro = models.DecimalField(default=0, verbose_name='Цена в евро', decimal_places=2, max_digits=5)
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=2, max_digits=5,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=2, max_digits=5,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.new_price_euro:
            return self.new_price_euro
        else:
            return self.price_euro

    def get_option_price_dollar(self):
        if self.new_price_dollar:
            return self.new_price_dollar
        else:
            return self.price_dollar

    class Meta:
        verbose_name = 'Обязательная опция'
        verbose_name_plural = 'Обязательные опции'


class RequiredOptionChild(models.Model):
    product = models.ForeignKey(Products, related_name='product_required_option_child', on_delete=models.PROTECT,
                                verbose_name='Товар')
    required_option = models.ForeignKey(RequiredOption, related_name='required_option_child', on_delete=models.PROTECT,
                                        verbose_name='Родительская')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price_dollar = models.DecimalField(default=0, verbose_name='Цена в долларах', decimal_places=2, max_digits=5)
    price_euro = models.DecimalField(default=0, verbose_name='Цена в евро', decimal_places=2, max_digits=5)
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=2, max_digits=5,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=2, max_digits=5,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.new_price_euro:
            return self.new_price_euro
        else:
            return self.price_euro

    def get_option_price_dollar(self):
        if self.price_dollar < 1:
            price = self.required_option.price_dollar * self.price_dollar
            return to_fixed(price, 2)
        if self.new_price_dollar:
            return self.new_price_dollar
        else:
            return self.price_dollar

    class Meta:
        verbose_name = 'Обязательная опция(дочерняя)'
        verbose_name_plural = 'Обязательные опции(дочерняя)'
        ordering = ['required_option']


class AdditionOptions(models.Model):
    product = models.ForeignKey(Products, related_name='product_addition_option', on_delete=models.PROTECT,
                                verbose_name='Товар')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    price_dollar = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='Цена в долларах')
    price_euro = models.DecimalField(default=0, decimal_places=2, max_digits=5, verbose_name='Цена в евро')
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=2, max_digits=5,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=2, max_digits=5,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.new_price_euro:
            return self.new_price_euro
        else:
            return self.price_euro

    def get_option_price_dollar(self):
        if self.new_price_dollar:
            return self.new_price_dollar
        else:
            return self.price_dollar

    class Meta:
        verbose_name = 'Дополнительная опция'
        verbose_name_plural = 'Дополнительные опции'

