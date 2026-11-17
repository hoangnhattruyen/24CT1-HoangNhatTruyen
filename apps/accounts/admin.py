
from django.contrib import admin
from .models import UserProfile, Address, StaffShift


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'role', 'phone']
    list_filter = ['role']

    @admin.display(description='EMAIL')
    def email(self, obj):
        return obj.user.email if obj.user else '-'


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'email', 'receiver_name', 'phone',
        'district', 'city', 'is_default'
    ]

    @admin.display(description='EMAIL')
    def email(self, obj):
        return obj.user.email if obj.user else '-'


@admin.register(StaffShift)
class StaffShiftAdmin(admin.ModelAdmin):
    list_display = [
        'staff',
        'shift_date',
        'check_in',
        'check_out',
        'orders_processed_count',
        'revenue_generated'
    ]
    list_filter = ['shift_date', 'staff']
