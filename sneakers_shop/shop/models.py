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
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'


class Manager(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} ({self.user.first_name} {self.user.last_name})'


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True)
    available_count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through="ProductInCart", blank=True, related_name='products_in_cart')

    def __str__(self):
        return f'Корзина пользователя {Client.objects.get(id=self.client_id.id).user.username}'


class Order(models.Model):
    delivery_date = models.DateTimeField()
    delivery_status = models.CharField(max_length=4, choices=DELIVERY_STATUS, default='PACK')
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    manager_id = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through="ProductInOrder", related_name='products_in_order')

    def __str__(self):
        return f'Заказ №{self.pk}'


class ProductInCart(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name='product_in_cart_fields')
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='product_in_cart_fields')
    product_count = models.IntegerField()


class ProductInOrder(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_count = models.IntegerField()


class Return(models.Model):
    reason = models.TextField()
    date = models.DateTimeField()
    status = models.CharField(max_length=7, choices=RETURN_STATUS, default='PENDING')
    client_id = models.OneToOneField(Client, on_delete=models.DO_NOTHING)
    manager_id = models.OneToOneField(Manager, on_delete=models.DO_NOTHING)
    order_id = models.OneToOneField(Order, on_delete=models.DO_NOTHING)
    product_id = models.OneToOneField(Product, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'Возврат №{self.pk}'
