from django.contrib import admin
from .models import Order, OrderGroup, OrderDetail

admin.site.register(Order)
admin.site.register(OrderGroup)
admin.site.register(OrderDetail)
