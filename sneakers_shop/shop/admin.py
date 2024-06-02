from django.contrib import admin

from shop.models import Client, Manager, Product, Order, Return, Cart, ProductInCart, ProductInOrder
admin.site.site_header = 'Админ-панель магазина "КРОССОВКИ.ру"'
# Register your models here.
admin.site.register(Client, list_display=['user', 'phone'])
admin.site.register(Manager)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Return)
admin.site.register(Cart)
admin.site.register(ProductInCart)
admin.site.register(ProductInOrder)
admin.site.site_header = 'Админ-панель магазина "КРОССОВКИ.ру"'