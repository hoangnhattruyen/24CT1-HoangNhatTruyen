from django.contrib import admin
from .models import UserProfile, Address, StaffShift

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'receiver_name', 'phone', 'district', 'city', 'is_default']

@admin.register(StaffShift)
class StaffShiftAdmin(admin.ModelAdmin):
    list_display = ['staff', 'shift_date', 'check_in', 'check_out', 'orders_processed_count', 'revenue_generated']
    list_filter = ['shift_date', 'staff']
