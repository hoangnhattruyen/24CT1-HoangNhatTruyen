from apps.products.models import Category
from apps.orders.models import Cart
from apps.stores.models import StoreLocation

def global_shop_data(request):
    """Cung cấp dữ liệu toàn cục cho Mega Menu, Giỏ hàng, Hotline trên mọi trang"""
    # Lấy danh mục cha và các danh mục con
    parent_categories = Category.objects.filter(parent__isnull=True, is_active=True).prefetch_related('children', 'brands')
    
    # Đếm số lượng sản phẩm trong giỏ hàng session
    cart_count = 0
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    try:
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user).first()
        else:
            cart = Cart.objects.filter(session_key=session_key).first()
            
        if cart:
            cart_count = sum(item.quantity for item in cart.items.all())
    except Exception:
        cart_count = 0
        
    total_stores = StoreLocation.objects.filter(is_active=True).count()
    if total_stores == 0:
        total_stores = 1164  # Con số thương hiệu Concung
        
    return {
        'global_categories': parent_categories,
        'global_cart_count': cart_count,
        'global_total_stores': total_stores,
        'global_hotline': '1800 6609',
    }
