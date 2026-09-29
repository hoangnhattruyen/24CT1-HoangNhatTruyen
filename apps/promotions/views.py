from django.shortcuts import render
from .models import FlashSale, Voucher

def promotions_list_view(request):
    flash_sales = FlashSale.objects.filter(is_active=True)
    vouchers = Voucher.objects.filter(is_active=True)
    return render(request, 'pages/promotions.html', {'flash_sales': flash_sales, 'vouchers': vouchers})
