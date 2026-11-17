from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class RegisterViewTests(TestCase):
    def test_register_rejects_blank_username_and_password(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'full_name': 'Test User',
                'username': '   ',
                'phone': '0901234567',
                'password': '   ',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username__iexact='   ').exists())
