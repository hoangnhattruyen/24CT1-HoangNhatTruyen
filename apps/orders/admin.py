
from django.contrib import admin, messages
from django.db import transaction
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import path

from .models import Cart, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'price', 'quantity', 'subtotal']

    fields = ['product_name', 'price', 'quantity', 'subtotal']

    def subtotal(self, obj):
        return obj.subtotal if obj else 0

    subtotal.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = [
        'order_code',
        'customer_name',
        'customer_phone',
        'total_amount',
        'payment_method',
        'payment_status',
        'status',
        'created_at',
    ]

    list_filter = [
        'status',
        'payment_method',
        'payment_status',
        'shipping_method',
        'created_at',
    ]

    search_fields = [
        'order_code',
        'customer_name',
        'customer_phone',
    ]

    readonly_fields = [
        'payment_confirmed_at',
        'payment_confirmed_by',
    ]

    inlines = [OrderItemInline]

    actions = ['confirm_qr_payment']

    @admin.action(description='Xác nhận đã nhận tiền QR')
    def confirm_qr_payment(self, request, queryset):

        success_count = 0

        for order_id in queryset.values_list('id', flat=True):

            with transaction.atomic():

                order = Order.objects.select_for_update().get(
                    id=order_id
                )

                if order.payment_method != 'QR':
                    continue

                if order.payment_status == 'PAID':
                    continue

                if order.status == 'CANCELLED':
                    continue

                # Kiểm tra tồn kho trước khi xác nhận
                valid_stock = True

                for item in order.items.select_related('product').all():
                    if item.product and item.product.stock < item.quantity:
                        valid_stock = False
                        break

                if not valid_stock:
                    self.message_user(
                        request,
                        f'Đơn {order.order_code}: Không đủ tồn kho.',
                        level=messages.ERROR
                    )
                    continue

                # Cập nhật tồn kho sau khi xác nhận thanh toán
                for item in order.items.select_related('product').all():
                    if item.product:
                        item.product.stock -= item.quantity
                        item.product.sold_count += item.quantity

                        item.product.save(
                            update_fields=['stock', 'sold_count']
                        )

                # Xác nhận thanh toán
                order.payment_status = 'PAID'
                order.payment_confirmed_at = timezone.now()
                order.payment_confirmed_by = request.user
                order.status = 'PROCESSING'

                order.save(
                    update_fields=[
                        'payment_status',
                        'payment_confirmed_at',
                        'payment_confirmed_by',
                        'status',
                        'updated_at',
                    ]
                )

                success_count += 1

        if success_count:
            self.message_user(
                request,
                f'Đã xác nhận thanh toán thành công {success_count} đơn hàng.',
                level=messages.SUCCESS
            )


# Đăng ký giỏ hàng
admin.site.register(Cart)
admin.site.register(CartItem)
