from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'first_name', 'last_name', 'income_type', 'is_profile_complete']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('phone', 'pan_number', 'income_type', 'city', 'state', 'is_profile_complete')}),)
