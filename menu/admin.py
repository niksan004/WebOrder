from django.contrib import admin
from .models import Dish, Category, Table, QrCode

admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Table)
admin.site.register(QrCode)
