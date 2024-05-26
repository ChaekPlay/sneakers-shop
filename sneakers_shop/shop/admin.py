from django.contrib import admin

from shop.models import Client, Manager, Product, Order, Return

# Register your models here.
admin.site.register(Client)
admin.site.register(Manager)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Return)