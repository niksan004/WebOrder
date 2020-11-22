from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cook, Distributor, Manager

admin.site.register(User, UserAdmin)
admin.site.register(Cook)
admin.site.register(Distributor)
admin.site.register(Manager)
