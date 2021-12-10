from .models import CustomUser
from django.contrib import admin


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'middle_name', 'email', 'password', 'role', 'is_active']  # add fields as you want


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(CustomUser)
