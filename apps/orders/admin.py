from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_code', 'customer_name', 'customer_phone', 'total_amount', 'shipping_method', 'status', 'created_at']
    list_filter = ['status', 'shipping_method', 'payment_method', 'created_at']
    search_fields = ['order_code', 'customer_name', 'customer_phone']
    inlines = [OrderItemInline]
