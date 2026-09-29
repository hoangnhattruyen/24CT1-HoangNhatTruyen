from django.shortcuts import render
from .models import StoreLocation

def store_locator_view(request):
    stores = StoreLocation.objects.filter(is_active=True).order_by('province', 'district', 'name')
    total_count = stores.count()
    return render(request, 'pages/stores.html', {
        'stores': stores,
        'total_count': total_count,
    })

