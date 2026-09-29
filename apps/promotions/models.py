from django.db import models
from apps.products.models import Product

class Banner(models.Model):
    POSITION_CHOICES = [
        ('TOP_ANNOUNCEMENT', 'Thanh thông báo trên cùng'),
        ('HERO', 'Hero Slider chính'),
        ('SUB_HERO', 'Banner phụ cạnh Hero'),
        ('CATEGORY', 'Banner danh mục'),
        ('FOOTER', 'Banner chân trang'),
    ]
    title = models.CharField(max_length=200, verbose_name="Tiêu đề Banner")
    image = models.FileField(upload_to='banners/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True)
    link_url = models.CharField(max_length=500, default='#', verbose_name="Đường dẫn đích")
    position = models.CharField(max_length=30, choices=POSITION_CHOICES, default='HERO')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Banner quảng cáo"
        verbose_name_plural = "Banner quảng cáo"
        ordering = ['order']

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        return self.image_url or "https://placehold.co/1200x400/FF82AB/FFFFFF?text=ConCung+Super+Sale"

    def __str__(self):
        return f"{self.title} ({self.get_position_display()})"

class FlashSale(models.Model):
    title = models.CharField(max_length=200, default="GIÁ SỐC MỖI NGÀY - DEAL CHỚP NHOÁNG", verbose_name="Tiêu đề Flash Sale")
    end_time = models.DateTimeField(verbose_name="Thời gian kết thúc (Countdown)")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    class Meta:
        verbose_name = "Flash Sale"
        verbose_name_plural = "Flash Sale"

    def __str__(self):
        return f"{self.title} (Hết hạn: {self.end_time.strftime('%d/%m/%Y %H:%M')})"

class FlashSaleItem(models.Model):
    flash_sale = models.ForeignKey(FlashSale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='flash_sales')
    flash_price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá sốc Flash Sale")
    quantity_limit = models.PositiveIntegerField(default=50, verbose_name="Số lượng bán")
    quantity_sold = models.PositiveIntegerField(default=15, verbose_name="Đã bán")

    @property
    def progress_percent(self):
        if self.quantity_limit > 0:
            return int((self.quantity_sold / self.quantity_limit) * 100)
        return 0

    def __str__(self):
        return f"{self.product.name} - Giá: {self.flash_price}"

class Voucher(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name="Mã giảm giá")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Số tiền giảm (VNĐ)")
    discount_percent = models.PositiveIntegerField(default=0, verbose_name="Hoặc giảm theo % (0-100)")
    min_order_value = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Đơn tối thiểu (VNĐ)")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Mã: {self.code}"
