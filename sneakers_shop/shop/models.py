from django.db import models

DELIVERY_STATUS = {
    'PACK': 'packing',
    'OTW': 'on the way',
    'DELD': 'delivered',
    'CANC': 'canceled',
}

RETURN_STATUS = {
    'ACCEPT': 'accepted',
    'DECLINE': 'declined',
}

# Create your models here.
class Client(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class Manager(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_count = models.IntegerField()


class Order(models.Model):
    delivery_date = models.DateTimeField()
    delivery_status = models.CharField(max_length=4,choices=DELIVERY_STATUS)
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
    status = models.CharField(max_length=7, choices=RETURN_STATUS)
    client_id = models.ForeignKey(Client, on_delete=models.DO_NOTHING)
    manager_id = models.ForeignKey(Manager, on_delete=models.DO_NOTHING)
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)





