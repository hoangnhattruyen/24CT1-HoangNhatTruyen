from django.db import models

class StoreLocation(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên siêu thị")
    province = models.CharField(max_length=100, default="TP. Hồ Chí Minh", verbose_name="Tỉnh / Thành phố")
    district = models.CharField(max_length=100, verbose_name="Quận / Huyện")
    address = models.CharField(max_length=300, verbose_name="Địa chỉ cụ thể")
    phone = models.CharField(max_length=20, default="1800 6609", verbose_name="Số điện thoại")
    opening_hours = models.CharField(max_length=100, default="08:00 - 22:00 (Tất cả các ngày trong tuần)", verbose_name="Giờ mở cửa")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Siêu thị Con Cưng"
        verbose_name_plural = "Hệ thống 1164 Siêu thị"
        ordering = ['province', 'district']

    def __str__(self):
        return f"{self.name} - {self.address}, {self.district}, {self.province}"
