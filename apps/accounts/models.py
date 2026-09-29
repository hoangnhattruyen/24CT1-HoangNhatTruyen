from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('CUSTOMER', 'Khách hàng'),
        ('STAFF', 'Nhân viên tư vấn & bán hàng'),
        ('ADMIN', 'Quản trị viên'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER', verbose_name="Vai trò")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Ngày sinh")
    baby_birth_date = models.DateField(blank=True, null=True, verbose_name="Ngày sinh bé / Ngày dự sinh")

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    receiver_name = models.CharField(max_length=150, verbose_name="Tên người nhận")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    city = models.CharField(max_length=100, default="TP. Hồ Chí Minh", verbose_name="Tỉnh/Thành")
    district = models.CharField(max_length=100, default="Quận 1", verbose_name="Quận/Huyện")
    street_address = models.CharField(max_length=255, verbose_name="Địa chỉ chi tiết")
    is_default = models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")

    class Meta:
        verbose_name = "Sổ địa chỉ"
        verbose_name_plural = "Sổ địa chỉ"

    def __str__(self):
        return f"{self.receiver_name} - {self.street_address}, {self.district}, {self.city}"

class StaffShift(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shifts', verbose_name="Nhân viên")
    shift_date = models.DateField(default=timezone.now, verbose_name="Ngày trực")
    check_in = models.DateTimeField(auto_now_add=True, verbose_name="Giờ Check-in")
    check_out = models.DateTimeField(null=True, blank=True, verbose_name="Giờ Check-out")
    orders_processed_count = models.PositiveIntegerField(default=0, verbose_name="Số đơn xử lý trong ca")
    revenue_generated = models.DecimalField(max_digits=12, decimal_places=0, default=0, verbose_name="Doanh thu ca trực (VNĐ)")
    notes = models.TextField(blank=True, verbose_name="Ghi chú ca trực")

    class Meta:
        verbose_name = "Ca trực nhân viên"
        verbose_name_plural = "Quản lý Check-in/Check-out nhân viên"
        ordering = ['-check_in']

    @property
    def is_active(self):
        return self.check_out is None

    def __str__(self):
        return f"{self.staff.username} - {self.shift_date} ({'Đang trực' if self.is_active else 'Đã kết thúc'})"
