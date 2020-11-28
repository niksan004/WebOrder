from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'email', 'is_cook', 'is_distributor', 'is_admin', 'is_active',)
    list_filter = ('username', 'email', 'is_cook', 'is_distributor', 'is_admin', 'is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        ('Permissions', {'fields': ('is_cook', 'is_distributor', 'is_admin', 'is_active',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_cook', 'is_distributor', 'is_admin', 'is_active',)}
        ),
    )


admin.site.register(User, CustomUserAdmin)
