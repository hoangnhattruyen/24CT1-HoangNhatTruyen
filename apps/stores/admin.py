from django.contrib import admin
from .models import StoreLocation

@admin.register(StoreLocation)
class StoreLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'district', 'province', 'phone', 'is_active']
    list_filter = ['province', 'district', 'is_active']
    search_fields = ['name', 'address', 'district']
