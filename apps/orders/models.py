from django.db import models
from django.contrib.auth.models import User
from apps.products.models import Product
from apps.promotions.models import Voucher

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=60, blank=True, null=True)
    voucher = models.ForeignKey(Voucher, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def raw_total(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def discount_amount(self):
        if not self.voucher:
            return 0
        if self.voucher.discount_amount > 0:
            return self.voucher.discount_amount
        if self.voucher.discount_percent > 0:
            return int((self.raw_total * self.voucher.discount_percent) / 100)
        return 0

    @property
    def total_price(self):
        t = self.raw_total - self.discount_amount
        return max(t, 0)

    @property
    def total_items_count(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Chờ xác nhận'),
        ('PROCESSING', 'Đã xác nhận & Đang chuẩn bị'),
        ('SHIPPING', 'Đang giao hàng (Siêu tốc 1h)'),
        ('DELIVERED', 'Đã giao hàng thành công'),
        ('CANCELLED', 'Đã hủy'),
    ]
    SHIPPING_CHOICES = [
        ('FAST_1H', 'Giao Siêu Tốc 1h'),
        ('STANDARD', 'Giao tiêu chuẩn (1-2 ngày)'),
    ]
    PAYMENT_CHOICES = [
        ('COD', 'Thanh toán tiền mặt (COD)'),
        ('VNPAY', 'Ví VNPAY / Ngân hàng QR'),
        ('MOMO', 'Ví MoMo'),
    ]
    order_code = models.CharField(max_length=30, unique=True, verbose_name="Mã đơn")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    staff_handler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handled_orders', verbose_name="Nhân viên xử lý")
    
    customer_name = models.CharField(max_length=150, verbose_name="Người nhận")
    customer_phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    shipping_address = models.CharField(max_length=300, verbose_name="Địa chỉ")
    city = models.CharField(max_length=100, default="TP. Hồ Chí Minh")
    district = models.CharField(max_length=100, default="Quận 1")
    note = models.TextField(blank=True)
    
    shipping_method = models.CharField(max_length=30, choices=SHIPPING_CHOICES, default='FAST_1H')
    payment_method = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='COD')
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.order_code} - {self.customer_name} ({self.get_status_display()})"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=0)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.price * self.quantity
