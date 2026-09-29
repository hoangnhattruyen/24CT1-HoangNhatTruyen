import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.products.models import Product
from apps.promotions.models import Voucher
from apps.accounts.models import Address
from .models import Cart, CartItem, Order, OrderItem

def get_or_create_cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'pages/cart.html', {'cart': cart})

def add_to_cart_view(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    
    return JsonResponse({
        'success': True,
        'message': f'Đã thêm {product.name} vào giỏ hàng!',
        'cart_count': cart.total_items_count,
        'total_price': f"{cart.total_price:,.0f}₫".replace(',', '.')
    })

def update_cart_item_view(request):
    item_id = request.POST.get('item_id')
    action = request.POST.get('action')
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'delete':
        item.delete()
        
    return redirect('orders:cart')

def apply_voucher_view(request):
    code = request.POST.get('voucher_code', '').strip().upper()
    cart = get_or_create_cart(request)
    voucher = Voucher.objects.filter(code=code, is_active=True).first()
    
    if voucher:
        if cart.raw_total >= voucher.min_order_value:
            cart.voucher = voucher
            cart.save()
            messages.success(request, f'Đã áp dụng mã giảm giá {code} thành công!')
        else:
            messages.error(request, f'Mã {code} chỉ áp dụng cho đơn hàng từ {voucher.min_order_value:,.0f}₫')
    else:
        messages.error(request, 'Mã giảm giá không hợp lệ hoặc đã hết hạn!')
    return redirect('orders:cart')

def checkout_view(request):
    cart = get_or_create_cart(request)
    if cart.items.count() == 0:
        return redirect('orders:cart')
        
    user_addresses = request.user.addresses.all() if request.user.is_authenticated else []
    default_address = user_addresses.filter(is_default=True).first()
    
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        phone = request.POST.get('customer_phone')
        address = request.POST.get('shipping_address')
        city = request.POST.get('city', 'TP. Hồ Chí Minh')
        district = request.POST.get('district', 'Quận 1')
        shipping_method = request.POST.get('shipping_method', 'FAST_1H')
        payment_method = request.POST.get('payment_method', 'COD')
        note = request.POST.get('note', '')
        
        shipping_fee = 0 if cart.total_price >= 249000 else 25000
        
        order = Order.objects.create(
            order_code=f"CC{uuid.uuid4().hex[:8].upper()}",
            user=request.user if request.user.is_authenticated else None,
            customer_name=name,
            customer_phone=phone,
            shipping_address=address,
            city=city,
            district=district,
            shipping_method=shipping_method,
            payment_method=payment_method,
            shipping_fee=shipping_fee,
            discount_amount=cart.discount_amount,
            total_amount=cart.total_price + shipping_fee,
            note=note
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity
            )
            # Trừ tồn kho & cộng số lượng đã bán
            item.product.stock = max(item.product.stock - item.quantity, 0)
            item.product.sold_count += item.quantity
            item.product.save()
            
        cart.items.all().delete()
        cart.voucher = None
        cart.save()
        return redirect('orders:order_success', order_code=order.order_code)
        
    return render(request, 'pages/checkout.html', {
        'cart': cart,
        'user_addresses': user_addresses,
        'default_address': default_address,
    })

def order_success_view(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    return render(request, 'pages/order_success.html', {'order': order})

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'pages/order_history.html', {'orders': orders})

def order_tracking_view(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    return render(request, 'pages/order_tracking.html', {'order': order})
