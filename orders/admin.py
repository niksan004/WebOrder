from django.contrib import admin
from .models import CooksOrders, DistributionOrders

admin.site.register(CooksOrders)
admin.site.register(DistributionOrders)
