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


class Manager(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_count = models.IntegerField(default=0)


class Order(models.Model):
    delivery_date = models.DateTimeField()
    delivery_status = models.CharField(max_length=4, choices=DELIVERY_STATUS, default='PACK')
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    manager_id = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through="ProductInOrder")


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





