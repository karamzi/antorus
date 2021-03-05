from django.db import models
from datetime import datetime
from os.path import splitext
from django.shortcuts import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.contrib.auth.models import User
import re


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
        if not self.slug:
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
        if not self.slug:
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
    product_order = models.SmallIntegerField(verbose_name='Порядок лота', default=0)
    image = models.ImageField(verbose_name='Изображение', upload_to=get_img_path)
    thumb = ThumbnailerImageField(upload_to=get_thumbs_path, verbose_name='Миниатюра',
                                  resize_source={'size': (120, 120), 'crop': True})
    slug = models.SlugField(verbose_name='Ссылка', blank=True, null=True)
    length = models.CharField(max_length=255, verbose_name='Длительность')
    char_req = models.CharField(max_length=255, verbose_name='Требования')
    price_dollar = models.DecimalField(verbose_name='Цена в долларах', decimal_places=3, max_digits=8, default=0)
    price_euro = models.DecimalField(verbose_name='Цена в евро', decimal_places=3, max_digits=8, default=0)
    quantity_required_options = models.IntegerField(verbose_name='max количество обязательных опций', blank=True,
                                                    null=True)
    quantity_required_child_options = models.IntegerField(verbose_name='max количество дочерних опций', blank=True,
                                                          null=True)
    quantity_addition_options = models.IntegerField(verbose_name='max количество доп опций', blank=True,
                                                    null=True)
    child_required = models.BooleanField(verbose_name='Дочернии обязательны', default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = self.name.strip()
            slug = slug.lower()
            slug = slug.replace(' ', '-')
            self.slug = slug
        super().save(*args, **kwargs)

    def get_price_dollar(self):
        return to_fixed(self.price_dollar, 2)

    def get_price_euro(self):
        return to_fixed(self.price_dollar, 2)

    def get_absolute_url(self):
        return reverse('product', kwargs={'slug': self.slug})

    def get_quantity_required_options(self):
        if self.quantity_required_options:
            return self.quantity_required_options
        return ''

    def get_quantity_required_child_options(self):
        if self.quantity_required_child_options:
            return self.quantity_required_child_options
        return ''

    def get_quantity_addition_options(self):
        if self.quantity_addition_options:
            return self.quantity_addition_options
        return ''

    def get_price_us(self):
        if self.price_dollar:
            return '$ ' + str(to_fixed(self.price_dollar, 2))
        else:
            req_options = self.product_required_option.all()
            min_price = 100000
            for item in req_options:
                if item.new_price_dollar and item.new_price_dollar < min_price:
                    min_price = item.new_price_dollar
                elif item.price_dollar < min_price:
                    min_price = item.price_dollar
            return 'from $ ' + str(to_fixed(min_price, 2))

    def get_price_eu(self):
        if self.price_euro:
            return '€ ' + str(to_fixed(self.price_dollar, 2))
        else:
            req_options = self.product_required_option.all()
            min_price = 100000
            for item in req_options:
                if item.new_price_euro and item.new_price_euro < min_price:
                    min_price = item.new_price_euro
                elif item.price_euro < min_price:
                    min_price = item.price_euro
            return 'from € ' + str(to_fixed(min_price, 2))

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['product_order']


class RequiredOption(models.Model):
    product = models.ForeignKey(Products, related_name='product_required_option', on_delete=models.PROTECT,
                                verbose_name='Товар')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    description = models.CharField(verbose_name='Описание', blank=True, max_length=255)
    price_dollar = models.DecimalField(default=0, verbose_name='Цена в долларах', decimal_places=3, max_digits=8)
    price_euro = models.DecimalField(default=0, verbose_name='Цена в евро', decimal_places=3, max_digits=8)
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=3, max_digits=8,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=3, max_digits=8,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.new_price_euro:
            return to_fixed(self.new_price_euro, 2)
        else:
            return to_fixed(self.price_euro, 2)

    def get_option_price_dollar(self):
        if self.new_price_dollar:
            return to_fixed(self.new_price_dollar, 2)
        else:
            return to_fixed(self.price_dollar, 2)

    class Meta:
        verbose_name = 'Обязательная опция'
        verbose_name_plural = 'Обязательные опции'


class RequiredOptionChild(models.Model):
    product = models.ForeignKey(Products, related_name='product_required_option_child', on_delete=models.PROTECT,
                                verbose_name='Товар')
    required_option = models.ForeignKey(RequiredOption, related_name='required_option_child', on_delete=models.PROTECT,
                                        verbose_name='Родительская')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    description = models.CharField(verbose_name='Описание', blank=True, max_length=255)
    price_dollar = models.DecimalField(default=0, verbose_name='Цена в долларах', decimal_places=3, max_digits=8)
    price_euro = models.DecimalField(default=0, verbose_name='Цена в евро', decimal_places=3, max_digits=8)
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=3, max_digits=8,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=3, max_digits=8,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.new_price_euro:
            return to_fixed(self.new_price_euro, 2)
        else:
            return to_fixed(self.price_euro, 2)

    def get_option_price_dollar(self):
        if self.price_dollar < 1:
            price = self.required_option.price_dollar * self.price_dollar
            return to_fixed(price, 2)
        if self.new_price_dollar:
            return to_fixed(self.new_price_dollar, 2)
        else:
            return to_fixed(self.price_dollar, 2)

    class Meta:
        verbose_name = 'Обязательная опция(дочерняя)'
        verbose_name_plural = 'Обязательные опции(дочерняя)'
        ordering = ['required_option']


class AdditionOptions(models.Model):
    product = models.ForeignKey(Products, related_name='product_addition_option', on_delete=models.PROTECT,
                                verbose_name='Товар')
    name = models.CharField(max_length=255, verbose_name='Название опции')
    description = models.CharField(verbose_name='Описание', blank=True, max_length=255)
    price_dollar = models.DecimalField(default=0, decimal_places=3, max_digits=8, verbose_name='Цена в долларах')
    price_euro = models.DecimalField(default=0, decimal_places=3, max_digits=8, verbose_name='Цена в евро')
    new_price_dollar = models.DecimalField(verbose_name='Цена со скидкой(долар)', decimal_places=3, max_digits=8,
                                           blank=True, null=True)
    new_price_euro = models.DecimalField(verbose_name='Цена со скидкой(евро)', decimal_places=3, max_digits=8,
                                         blank=True, null=True)

    def __str__(self):
        return self.name

    def get_option_price_euro(self):
        if self.price_euro < 1:
            return 0
        if self.new_price_euro:
            return to_fixed(self.new_price_euro, 2)
        else:
            return to_fixed(self.price_euro, 2)

    def get_option_price_dollar(self):
        if self.price_dollar < 1:
            return 0
        if self.new_price_dollar:
            return to_fixed(self.new_price_dollar, 2)
        else:
            return to_fixed(self.price_dollar, 2)

    class Meta:
        verbose_name = 'Дополнительная опция'
        verbose_name_plural = 'Дополнительные опции'


class Cart(models.Model):
    product = models.CharField(max_length=255, verbose_name='Товар')
    price = models.CharField(verbose_name='Цена', max_length=50)
    quantity = models.SmallIntegerField(verbose_name='Количество')
    total = models.CharField(verbose_name='Итого', max_length=50)
    order = models.ForeignKey('Order', on_delete=models.PROTECT, verbose_name='Заказ', related_name='order_product')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'Товар(заказа)'
        verbose_name_plural = 'Товары(заказа)'
        ordering = ['-product']


class CartOptions(models.Model):
    product = models.ForeignKey(Cart, on_delete=models.PROTECT, verbose_name='Товар', related_name='cart_cart_options')
    order = models.ForeignKey('Order', on_delete=models.PROTECT, verbose_name='Заказ',
                              related_name='order_cart_options')
    name = models.CharField(verbose_name='Опция', max_length=255)
    price = models.CharField(verbose_name='Цена', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Опция'
        verbose_name_plural = 'Опции'
        ordering = ['product']


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Пользователь', null=True,
                             related_name='user_order')
    character_server = models.CharField(max_length=255, verbose_name='Персонаж и Сервер')
    battle_tag = models.CharField(max_length=50, verbose_name='Battle tag', blank=True)
    faction = models.CharField(max_length=50, verbose_name='Фракция')
    connection = models.CharField(max_length=255, verbose_name='Skype или Discord')
    email = models.EmailField(verbose_name='Почта')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    STATUS = (
        ('1', 'CREATED'),
        ('2', 'PAID'),
        ('3', 'PAYMENT ERROR'),
        ('4', 'PROCESSING'),
        ('5', 'COMPLETED'),
    )
    status = models.CharField(verbose_name='Статус заказа', choices=STATUS, max_length=100)
    price = models.CharField(verbose_name='Без купона', max_length=50)
    coupon = models.CharField(verbose_name='Купон', max_length=50, blank=True)
    total = models.CharField(verbose_name='Итого', max_length=50)
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', null=True)

    def __str__(self):
        return 'Заказ № ' + str(self.id + 1000)

    def get_discount(self):
        reg = r'[0-9.]+'
        reg2 = r'[$€]'
        price = re.findall(reg, self.price)[0]
        total = re.findall(reg, self.total)[0]
        sing = re.findall(reg2, self.price)[0]
        coupon = float(price) - float(total)
        return '{} {:.2f}'.format(sing, coupon)

    def get_order_number(self):
        return str(self.id + 1000)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Coupon(models.Model):
    name = models.CharField(max_length=50, verbose_name='Купон')
    discount = models.SmallIntegerField(default=0, verbose_name='Процент скидки')
    count = models.SmallIntegerField(default=0, verbose_name='Количество использований', editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'


class BestOffersToday(models.Model):
    product = models.OneToOneField(Products, on_delete=models.PROTECT, verbose_name='Товар')
    product_order = models.SmallIntegerField(default=0, verbose_name='Порядок лотов')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Лучшее предложение'
        verbose_name_plural = 'Лучшие предложения'
        ordering = ['product_order']


class AuthToken(models.Model):
    token = models.TextField(verbose_name='Токен')
    time_created = models.DateTimeField(auto_now_add=True, verbose_name='Время создения')

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'


class Transactions(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', related_name='order_transactions', on_delete=models.PROTECT)
    SERVICE = (
        ('1', 'Fondy'),
    )
    service = models.CharField(max_length=50, verbose_name='Сервис оплаты', choices=SERVICE)
    status = models.CharField(max_length=20, verbose_name='Статус оплаты')
    currency = models.CharField(max_length=10, verbose_name='Валюта')
    amount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name='Сумма')
    date = models.DateTimeField(verbose_name='Дата транзакции', auto_now_add=True)
    response = models.TextField(verbose_name='Ответ от сервера', blank=True)

    def __str__(self):
        return 'Заказ №' + self.order.get_order_number()

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-date']
