from django.contrib import admin

from .models import Customer, Order, Carrier

admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Carrier)