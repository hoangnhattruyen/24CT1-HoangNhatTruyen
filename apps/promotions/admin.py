from django.contrib import admin
from .models import Banner, FlashSale, FlashSaleItem, Voucher

class FlashSaleItemInline(admin.TabularInline):
    model = FlashSaleItem
    extra = 2

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'order', 'is_active']
    list_filter = ['position', 'is_active']

@admin.register(FlashSale)
class FlashSaleAdmin(admin.ModelAdmin):
    list_display = ['title', 'end_time', 'is_active']
    inlines = [FlashSaleItemInline]

@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_amount', 'discount_percent', 'min_order_value', 'is_active']
