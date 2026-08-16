from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom Admin interface for User model.
    Extends standard Django UserAdmin to include phone_number, profile_picture, and bio.
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('ZENZEE Profile Info', {'fields': ('phone_number', 'profile_picture', 'bio')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('ZENZEE Profile Info', {'fields': ('phone_number', 'profile_picture', 'bio')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff')
    search_fields = ('username', 'email', 'phone_number', 'first_name', 'last_name')
