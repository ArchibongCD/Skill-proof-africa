# users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for CustomUser
    """
    list_display = ['username', 'email', 'wallet_address', 'country', 'created_at']
    search_fields = ['username', 'email', 'wallet_address']
    list_filter = ['country', 'created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Blockchain Info', {'fields': ('wallet_address',)}),
        ('Additional Info', {'fields': ('bio', 'country', 'phone')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Blockchain Info', {'fields': ('wallet_address',)}),
        ('Additional Info', {'fields': ('bio', 'country', 'phone')}),
    )