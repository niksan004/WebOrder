from django.contrib import admin
from .models import Dish, Category, Table, QrCode, Comment, Allergen

admin.site.register(Dish)
admin.site.register(Category)
admin.site.register(Table)
admin.site.register(QrCode)
admin.site.register(Comment)
admin.site.register(Allergen)
