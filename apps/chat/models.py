from django.db import models
from django.contrib.auth.models import User

class ChatSession(models.Model):
    MODE_CHOICES = [
        ('AI', 'Trợ lý AI Mẹ & Bé 24/7'),
        ('STAFF', 'Nhân viên CSKH trực tuyến'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_sessions')
    customer_name = models.CharField(max_length=150, default="Khách hàng Con Cưng")
    session_key = models.CharField(max_length=60, blank=True)
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='handling_chats')
    chat_mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='AI', verbose_name="Chế độ Chat")
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Chat #{self.id} - {self.customer_name} ({self.get_chat_mode_display()})"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sender_name = models.CharField(max_length=150)
    is_staff = models.BooleanField(default=False)
    is_ai = models.BooleanField(default=False, verbose_name="Tin nhắn từ AI")
    message = models.TextField()
    suggested_products_json = models.JSONField(null=True, blank=True, verbose_name="Danh sách SP gợi ý (JSON)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_name}: {self.message[:30]}"
