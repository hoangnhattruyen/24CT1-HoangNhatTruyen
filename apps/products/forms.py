
from django import forms
from django.utils.text import slugify
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = [
            'category',
            'brand',
            'name',
            'sku',
            'main_image_url',
            'price',
            'original_price',
            'stock',
            'is_fast_delivery_1h',
            'gift_description',
            'age_group',
            'origin',
            'description',
            'rating',
            'review_count',
            'is_featured',
            'is_active',
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'main_image_url': forms.URLInput(attrs={
                'placeholder': 'https://example.com/image.jpg'
            }),
            'price': forms.NumberInput(attrs={'min': 0}),
            'original_price': forms.NumberInput(attrs={'min': 0}),
            'stock': forms.NumberInput(attrs={'min': 0}),
            'rating': forms.NumberInput(attrs={
                'min': 0, 'max': 5, 'step': '0.1'
            }),
            'review_count': forms.NumberInput(attrs={'min': 0}),
        }

    def save(self, commit=True):
        product = super().save(commit=False)

        # Tạo slug duy nhất theo tên sản phẩm
        base_slug = slugify(product.name) or 'san-pham'
        unique_slug = base_slug
        counter = 1

        queryset = Product.objects.all()
        if product.pk:
            queryset = queryset.exclude(pk=product.pk)

        while queryset.filter(slug=unique_slug).exists():
            unique_slug = f'{base_slug}-{counter}'
            counter += 1

        product.slug = unique_slug

        if commit:
            product.save()
            self.save_m2m()

        return product
