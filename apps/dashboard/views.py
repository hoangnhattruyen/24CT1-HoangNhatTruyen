from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from apps.orders.models import Order, OrderItem
from apps.products.models import Product, ProductReview
from apps.accounts.models import StaffShift, UserProfile
from apps.chat.models import ChatSession, ChatMessage

# ---------- A. PHÂN HỆ DÀNH CHO NHÂN VIÊN ----------
@login_required
def staff_dashboard_view(request):
    if not (request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role in ['STAFF', 'ADMIN'])):
        messages.error(request, 'Bạn cần đăng nhập bằng tài khoản nhân viên.')
        return redirect('accounts:login')

    today = timezone.now().date()
    current_shift = StaffShift.objects.filter(staff=request.user, check_out__isnull=True).first()
    
    today_orders = Order.objects.filter(created_at__date=today)
    products_sold_today = OrderItem.objects.filter(order__created_at__date=today).aggregate(Sum('quantity'))['quantity__sum'] or 0
    revenue_today = int(today_orders.aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
    
    pending_orders = Order.objects.filter(status__in=['PENDING', 'PROCESSING']).order_by('-created_at')[:10]
    products_stock = Product.objects.filter(is_active=True).order_by('stock')[:10]
    open_chats = ChatSession.objects.filter(is_resolved=False).order_by('-updated_at')[:5]

    context = {
        'current_shift': current_shift,
        'products_sold_today': products_sold_today,
        'revenue_today': revenue_today,
        'pending_orders': pending_orders,
        'products_stock': products_stock,
        'open_chats': open_chats,
    }
    return render(request, 'dashboard/staff_dashboard.html', context)

@login_required
def staff_update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    new_status = request.POST.get('status')
    if new_status in dict(Order.STATUS_CHOICES):
        order.status = new_status
        order.staff_handler = request.user
        order.save()
        messages.success(request, f'Đã cập nhật trạng thái đơn #{order.order_code} thành {order.get_status_display()}')
    return redirect('dashboard:staff_dashboard')

@login_required
def staff_chat_view(request, session_id):
    session = get_object_or_404(ChatSession, id=session_id)
    if request.method == 'POST':
        text = request.POST.get('message', '').strip()
        if text:
            ChatMessage.objects.create(
                session=session,
                sender=request.user,
                sender_name=f"CSKH ({request.user.first_name or request.user.username})",
                is_staff=True,
                is_ai=False,
                message=text
            )
            session.staff = request.user
            session.chat_mode = 'STAFF'
            session.save()
            return redirect('dashboard:staff_chat', session_id=session.id)
            
    return render(request, 'dashboard/staff_chat_detail.html', {'chat_session': session})

# ---------- B. PHÂN HỆ DÀNH CHO ADMIN ----------
@login_required
def admin_dashboard_view(request):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')):
        messages.error(request, 'Chỉ Quản trị viên (Admin) mới có quyền truy cập.')
        return redirect('products:index')
        
    now = timezone.now()
    today = now.date()
    start_week = today - timedelta(days=today.weekday())
    start_month = today.replace(day=1)
    
    rev_day = int(Order.objects.filter(created_at__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
    rev_week = int(Order.objects.filter(created_at__date__gte=start_week).aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
    rev_month = int(Order.objects.filter(created_at__date__gte=start_month).aggregate(Sum('total_amount'))['total_amount__sum'] or 0)
    
    staff_users = User.objects.filter(profile__role__in=['STAFF', 'ADMIN']).order_by('-date_joined')
    recent_shifts = StaffShift.objects.order_by('-check_in')[:10]
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lte=15, is_active=True).order_by('stock')
    recent_reviews = ProductReview.objects.order_by('-created_at')[:10]
    all_orders = Order.objects.order_by('-created_at')[:15]

    context = {
        'rev_day': rev_day,
        'rev_week': rev_week,
        'rev_month': rev_month,
        'staff_users': staff_users,
        'recent_shifts': recent_shifts,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'recent_reviews': recent_reviews,
        'all_orders': all_orders,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def admin_create_account_view(request):
    """Chức năng tạo riêng tài khoản Nhân viên (Staff) hoặc Quản trị viên (Admin)"""
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')):
        messages.error(request, 'Chỉ Admin mới có quyền tạo tài khoản quản trị.')
        return redirect('products:index')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        role = request.POST.get('role', 'STAFF') # STAFF hoặc ADMIN
        
        if User.objects.filter(username=username).exists():
            messages.error(request, f'Tên đăng nhập "{username}" đã tồn tại trên hệ thống!')
        else:
            is_staff = True
            is_superuser = (role == 'ADMIN')
            
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=full_name,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            UserProfile.objects.create(
                user=user,
                role=role,
                phone=phone
            )
            messages.success(request, f'Đã tạo thành công tài khoản {role}: {username} ({full_name})!')
            return redirect('dashboard:admin_staff_manage')
            
    return render(request, 'dashboard/admin_create_account.html')

@login_required
def admin_staff_manage_view(request):
    """Quản lý toàn bộ danh sách tài khoản Nhân viên & Admin"""
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')):
        return redirect('products:index')
        
    staff_list = User.objects.filter(profile__role__in=['STAFF', 'ADMIN']).select_related('profile').order_by('-date_joined')
    return render(request, 'dashboard/admin_staff_manage.html', {'staff_list': staff_list})

@login_required
def admin_toggle_staff_status(request, user_id):
    """Khóa / Mở khóa tài khoản nhân viên"""
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')):
        return redirect('products:index')
        
    user_obj = get_object_or_404(User, id=user_id)
    if user_obj.is_superuser and user_obj == request.user:
        messages.error(request, 'Không thể tự khóa tài khoản Admin của chính mình!')
    else:
        user_obj.is_active = not user_obj.is_active
        user_obj.save()
        status_str = "Kích hoạt" if user_obj.is_active else "Khóa tạm thời"
        messages.success(request, f'Đã {status_str} tài khoản {user_obj.username}!')
        
    return redirect('dashboard:admin_staff_manage')

@login_required
def admin_toggle_review(request, review_id):
    if not (request.user.is_superuser or (hasattr(request.user, 'profile') and request.user.profile.role == 'ADMIN')):
        return redirect('products:index')
    review = get_object_or_404(ProductReview, id=review_id)
    review.is_approved = not review.is_approved
    review.save()
    messages.success(request, f'Đã {"Duyệt" if review.is_approved else "Ẩn"} đánh giá của {review.user.username}')
    return redirect('dashboard:admin_dashboard')
