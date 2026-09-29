from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    icon = models.CharField(max_length=100, blank=True, verbose_name="Icon đại diện")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="Danh mục cha")
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")

    class Meta:
        verbose_name = "Danh mục sản phẩm"
        verbose_name_plural = "Danh mục sản phẩm"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=120, verbose_name="Tên thương hiệu")
    slug = models.SlugField(max_length=130, unique=True, blank=True)
    logo_url = models.URLField(max_length=500, blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='brands')
    is_featured = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Thương hiệu"
        verbose_name_plural = "Thương hiệu"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    AGE_CHOICES = [
        ('ALL', 'Mọi độ tuổi'),
        ('0_1', '0 - 1 tuổi'),
        ('1_2', '1 - 2 tuổi'),
        ('2_PLUS', 'Trên 2 tuổi'),
        ('MOM', 'Mẹ bầu & Sau sinh'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm")
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    sku = models.CharField(max_length=50, unique=True, verbose_name="Mã SKU")
    main_image_url = models.URLField(max_length=500, blank=True)
    
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name="Giá bán niêm yết")
    original_price = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name="Giá gốc thị trường")
    stock = models.PositiveIntegerField(default=100, verbose_name="Số lượng tồn kho")
    sold_count = models.PositiveIntegerField(default=0, verbose_name="Số lượng đã bán")
    
    is_fast_delivery_1h = models.BooleanField(default=True, verbose_name="Giao 1h")
    gift_description = models.CharField(max_length=255, blank=True, verbose_name="Quà tặng kèm")
    age_group = models.CharField(max_length=20, choices=AGE_CHOICES, default='ALL', verbose_name="Độ tuổi phù hợp")
    origin = models.CharField(max_length=100, blank=True, verbose_name="Xuất xứ")
    
    description = models.TextField(blank=True, verbose_name="Chi tiết sản phẩm")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=5.0, verbose_name="Đánh giá sao")
    review_count = models.PositiveIntegerField(default=0, verbose_name="Lượt đánh giá")
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
        ordering = ['-created_at']

    @property
    def discount_percent(self):
        if self.original_price and self.original_price > self.price:
            return int(round(((self.original_price - self.price) / self.original_price) * 100))
        return 0

    @property
    def display_image(self):
        return self.main_image_url or "https://placehold.co/400x400/FFE7BA/FF82AB?text=ConCung"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Sản phẩm")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', verbose_name="Khách hàng")
    rating = models.PositiveIntegerField(default=5, verbose_name="Số sao (1-5)")
    comment = models.TextField(verbose_name="Nội dung đánh giá / Feedback")
    is_approved = models.BooleanField(default=True, verbose_name="Duyệt hiển thị")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Đánh giá & Feedback"
        verbose_name_plural = "Quản lý Đánh giá & Feedback"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.product.name} ({self.rating} sao)"
