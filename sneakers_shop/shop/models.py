from django.contrib.auth.models import User
from django.db import models
from django.db.models import OneToOneField

DELIVERY_STATUS = [
    ('PACK', 'packing'),
    ('OTW', 'on the way'),
    ('DELD', 'delivered'),
    ('CANC', 'canceled')
]

RETURN_STATUS = [
    ('PENDING', 'pending'),
    ('ACCEPT', 'accepted'),
    ('DECLINE', 'declined'),
]


# Create your models here.
class Client(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
    def __str__(self):
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'\



class Manager(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'
    def __str__(self):
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание')
    size = models.CharField(max_length=20, verbose_name='Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    image = models.ImageField(upload_to='images/', null=True, verbose_name='Изображение')
    available_count = models.IntegerField(default=0, verbose_name='Доступное количество')
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    products = models.ManyToManyField(Product, through="ProductInCart", blank=True, related_name='products_in_cart', verbose_name='Товары')
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    def __str__(self):
        return f'Корзина пользователя {Client.objects.get(id=self.client.id).user.username}'


class Order(models.Model):
    delivery_date = models.DateTimeField(verbose_name='Дата доставки')
    delivery_status = models.CharField(max_length=4, choices=DELIVERY_STATUS, default='PACK', verbose_name='Статус доставки')
    delivery_address = models.CharField(max_length=255, verbose_name='Адрес доставки')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    manager = models.ForeignKey(Manager, on_delete=models.DO_NOTHING, verbose_name='Менеджер')
    products = models.ManyToManyField(Product, through="ProductInOrder", related_name='products_in_order', verbose_name='Товары')
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
    def __str__(self):
        return f'Заказ №{self.pk}'


class ProductInCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='product_in_cart_fields', verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_in_cart_fields', verbose_name='Товар')
    product_count = models.IntegerField(verbose_name='Количество')
    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'
    def __str__(self):
        return f'Товар {self.product.name} в корзине пользователя {Client.objects.get(id=self.cart.client.id).user.username}'

class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    product_count = models.IntegerField(verbose_name='Количество')
    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказах'
    def __str__(self):
        return f'Товар {self.product.name} в заказе №{self.order.id} пользователя {Client.objects.get(id=self.order.client.id).user.username}'

class Return(models.Model):
    reason = models.TextField(verbose_name='Причина возврата')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата возврата')
    status = models.CharField(max_length=7, choices=RETURN_STATUS, default='PENDING', verbose_name='Статус возврата')
    client = models.ForeignKey(Client, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    manager = models.ForeignKey(Manager, on_delete=models.DO_NOTHING, verbose_name='Менеджер')
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, verbose_name='Товар')
    class Meta:
        verbose_name = 'Возврат'
        verbose_name_plural = 'Возвраты'
    def __str__(self):
        return f'Возврат №{self.pk}'
