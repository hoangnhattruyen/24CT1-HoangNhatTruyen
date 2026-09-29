from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import UserProfile, Address, StaffShift
from apps.orders.models import Order

def register_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        phone = request.POST.get('phone', '')
        name = request.POST.get('full_name', '')
        
        if User.objects.filter(username=u).exists():
            messages.error(request, 'Tên đăng nhập đã tồn tại!')
        else:
            user = User.objects.create_user(username=u, password=p, first_name=name)
            UserProfile.objects.create(user=user, phone=phone, role='CUSTOMER')
            login(request, user)
            messages.success(request, 'Đăng ký tài khoản thành công!')
            return redirect('products:index')
    return render(request, 'pages/register.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            messages.success(request, f'Chào mừng {user.first_name or user.username} quay trở lại!')
            
            # Nếu là nhân viên hoặc admin -> Chuyển hướng tới dashboard tương ứng
            if hasattr(user, 'profile') and user.profile.role == 'STAFF':
                return redirect('dashboard:staff_dashboard')
            elif user.is_superuser or (hasattr(user, 'profile') and user.profile.role == 'ADMIN'):
                return redirect('dashboard:admin_dashboard')
            return redirect('products:index')
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    return render(request, 'pages/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Đã đăng xuất tài khoản!')
    return redirect('products:index')

@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    addresses = request.user.addresses.all()
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'update_profile':
            request.user.first_name = request.POST.get('full_name', '')
            request.user.email = request.POST.get('email', '')
            request.user.save()
            profile.phone = request.POST.get('phone', '')
            profile.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('accounts:profile')
            
        elif action == 'add_address':
            receiver = request.POST.get('receiver_name')
            phone = request.POST.get('phone')
            street = request.POST.get('street_address')
            city = request.POST.get('city')
            district = request.POST.get('district')
            is_default = request.POST.get('is_default') == 'on'
            
            if is_default:
                Address.objects.filter(user=request.user).update(is_default=False)
            Address.objects.create(
                user=request.user, receiver_name=receiver, phone=phone,
                street_address=street, city=city, district=district, is_default=is_default
            )
            messages.success(request, 'Thêm địa chỉ giao hàng thành công!')
            return redirect('accounts:profile')
            
    return render(request, 'pages/customer_profile.html', {
        'profile': profile,
        'addresses': addresses,
        'recent_orders': recent_orders,
    })

@login_required
def staff_checkin_checkout_toggle(request):
    if not (request.user.is_staff or (hasattr(request.user, 'profile') and request.user.profile.role in ['STAFF', 'ADMIN'])):
        messages.error(request, 'Bạn không có quyền thực hiện chức năng này.')
        return redirect('products:index')
        
    active_shift = StaffShift.objects.filter(staff=request.user, check_out__isnull=True).first()
    if active_shift:
        active_shift.check_out = timezone.now()
        active_shift.save()
        messages.success(request, f'Đã Check-out ca trực lúc {active_shift.check_out.strftime("%H:%M:%S")}!')
    else:
        shift = StaffShift.objects.create(staff=request.user)
        messages.success(request, f'Đã Check-in ca trực thành công lúc {shift.check_in.strftime("%H:%M:%S")}!')
    return redirect('dashboard:staff_dashboard')
