from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/apply-voucher/', views.apply_voucher_view, name='apply_voucher'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<str:order_code>/', views.order_success_view, name='order_success'),
    path('history/', views.order_history_view, name='order_history'),
    path('track/<str:order_code>/', views.order_tracking_view, name='order_tracking'),
]
