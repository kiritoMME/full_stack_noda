from django.contrib import admin
from .models import Product, Tag, Order, ConfirmedOrder
# Register your models here.

admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Order)
admin.site.register(ConfirmedOrder)