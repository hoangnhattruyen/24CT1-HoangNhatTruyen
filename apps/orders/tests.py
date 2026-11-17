from django.test import TestCase
from django.urls import reverse

from apps.products.models import Product


class CartViewTests(TestCase):
    def test_add_to_cart_rejects_invalid_quantity(self):
        product = Product.objects.first()
        if product is None:
            self.skipTest('No product found in database for cart test.')

        response = self.client.post(
            reverse('orders:add_to_cart'),
            {'product_id': product.id, 'quantity': 'abc'},
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('Số lượng không hợp lệ', response.json()['message'])
