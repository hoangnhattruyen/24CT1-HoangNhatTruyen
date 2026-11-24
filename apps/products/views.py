from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q, Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Brand, Product, ProductReview
from apps.promotions.models import Banner, FlashSale
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from apps.accounts.models import UserProfile
from .forms import ProductForm


# Kiểm tra tài khoản có vai trò ADMIN hoặc STAFF
def is_admin_or_staff(user):
    if not user.is_authenticated:
        return False

    try:
        return user.profile.role in ['ADMIN', 'STAFF']
    except UserProfile.DoesNotExist:
        return False


# Chỉ ADMIN mới được thêm, sửa, xóa sản phẩm
def is_admin(user):
    if not user.is_authenticated:
        return False

    try:
        return user.profile.role == 'ADMIN'
    except UserProfile.DoesNotExist:
        return False

def index_view(request):
    banners = Banner.objects.filter(is_active=True, position='HERO')[:4]
    sub_banners = Banner.objects.filter(is_active=True, position='SUB_HERO')[:2]
    flash_sale = FlashSale.objects.filter(is_active=True).first()
    
    categories = Category.objects.filter(parent__isnull=True, is_active=True)[:9]
    best_sellers = Product.objects.filter(is_active=True).order_by('-sold_count')[:4]
    top_rated = Product.objects.filter(is_active=True).order_by('-rating')[:4]
    latest_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    brands = Brand.objects.filter(is_featured=True)[:12]
    
    context = {
        'banners': banners,
        'sub_banners': sub_banners,
        'flash_sale': flash_sale,
        'categories': categories,
        'best_sellers': best_sellers,
        'top_rated': top_rated,
        'latest_products': latest_products,
        'brands': brands,
    }
    return render(request, 'pages/index.html', context)

def category_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    sub_cats = category.children.all()
    cat_ids = [category.id] + list(sub_cats.values_list('id', flat=True))
    
    products = Product.objects.filter(category_id__in=cat_ids, is_active=True)
    
    # Lọc theo thương hiệu
    brand_slug = request.GET.get('brand')
    if brand_slug:
        products = products.filter(brand__slug=brand_slug)
        
    # Lọc theo độ tuổi
    age = request.GET.get('age')
    if age:
        products = products.filter(age_group=age)
        
    # Lọc theo giá
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    if price_min:
        products = products.filter(price__gte=price_min)
    if price_max:
        products = products.filter(price__lte=price_max)
        
    sort = request.GET.get('sort', '-created_at')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')
    elif sort == 'best_seller':
        products = products.order_by('-sold_count')
    elif sort == 'top_rated':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')
        
    available_brands = Brand.objects.filter(products__category_id__in=cat_ids).distinct()
    
    context = {
        'category': category,
        'products': products,
        'available_brands': available_brands,
        'current_brand': brand_slug,
        'current_age': age,
        'current_sort': sort,
    }
    return render(request, 'pages/category.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    reviews = product.reviews.filter(is_approved=True)
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'pages/product_detail.html', context)

@login_required
def add_review_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')
        ProductReview.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment
        )
        # Cập nhật lại rating trung bình của sản phẩm
        avg_rating = product.reviews.filter(is_approved=True).aggregate(Avg('rating'))['rating__avg']
        if avg_rating:
            product.rating = round(avg_rating, 1)
            product.review_count = product.reviews.filter(is_approved=True).count()
            product.save()
            
        messages.success(request, 'Cảm ơn bạn đã gửi đánh giá sản phẩm!')
    return redirect('products:product_detail', slug=product.slug)

def best_sellers_view(request):
    products = Product.objects.filter(is_active=True).order_by('-sold_count')[:24]
    return render(request, 'pages/product_list_special.html', {
        'title': '🔥 SẢN PHẨM BÁN CHẠY NHẤT (BEST SELLERS)',
        'products': products
    })

def top_rated_view(request):
    products = Product.objects.filter(is_active=True).order_by('-rating', '-review_count')[:24]
    return render(request, 'pages/product_list_special.html', {
        'title': '⭐ SẢN PHẨM CÓ ĐÁNH GIÁ CAO NHẤT',
        'products': products
    })

def search_api_view(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(brand__name__icontains=query) | Q(category__name__icontains=query),
            is_active=True
        )[:6]
        for p in products:
            results.append({
                'id': p.id,
                'name': p.name,
                'price': f"{p.price:,.0f}₫".replace(',', '.'),
                'image': p.display_image,
                'url': f"/product/{p.slug}/",
            })
    return JsonResponse({'results': results})


# ==========================================
# QUẢN LÝ SẢN PHẨM
# ==========================================

# ADMIN và STAFF được xem danh sách sản phẩm
@user_passes_test(is_admin_or_staff)
def admin_product_list_view(request):
    products = Product.objects.select_related(
        'category', 'brand'
    ).all()

    # Tìm kiếm sản phẩm
    keyword = request.GET.get('q', '').strip()

    if keyword:
        products = products.filter(
            Q(name__icontains=keyword)
            | Q(sku__icontains=keyword)
            | Q(category__name__icontains=keyword)
            | Q(brand__name__icontains=keyword)
        )

    # Lọc trạng thái
    status = request.GET.get('status', '')

    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)

    # Phân trang
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    context = {
        'products': page_obj,
        'keyword': keyword,
        'current_status': status,

        # Thống kê
        'total_products': Product.objects.count(),
        'active_count': Product.objects.filter(
            is_active=True
        ).count(),
        'inactive_count': Product.objects.filter(
            is_active=False
        ).count(),

        # Phân quyền
        'is_admin': request.user.profile.role == 'ADMIN',
    }

    return render(
        request,
        'pages/admin_products.html',
        context
    )


# ==========================================
# THÊM SẢN PHẨM
# ==========================================

@user_passes_test(is_admin)
def admin_product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f'Đã thêm sản phẩm "{product.name}" thành công!'
            )

            return redirect('products:admin_product_list')

        messages.error(
            request,
            'Vui lòng kiểm tra lại thông tin sản phẩm.'
        )

    else:
        form = ProductForm()

    context = {
        'form': form,
        'page_title': 'THÊM SẢN PHẨM MỚI',
        'submit_text': 'Lưu sản phẩm',
    }

    return render(
        request,
        'pages/admin_product_form.html',
        context
    )


# ==========================================
# SỬA SẢN PHẨM
# ==========================================

@user_passes_test(is_admin)
def admin_product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():
            updated_product = form.save()

            messages.success(
                request,
                f'Đã cập nhật sản phẩm "{updated_product.name}" thành công!'
            )

            return redirect('products:admin_product_list')

        messages.error(
            request,
            'Vui lòng kiểm tra lại thông tin sản phẩm.'
        )

    else:
        form = ProductForm(instance=product)

    context = {
        'form': form,
        'product': product,
        'page_title': 'CẬP NHẬT SẢN PHẨM',
        'submit_text': 'Cập nhật sản phẩm',
    }

    return render(
        request,
        'pages/admin_product_form.html',
        context
    )


# ==========================================
# XÓA SẢN PHẨM
# ==========================================

@user_passes_test(is_admin)
def admin_product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_name = product.name

        try:
            product.delete()

            messages.success(
                request,
                f'Đã xóa sản phẩm "{product_name}" thành công!'
            )

        except Exception:
            messages.error(
                request,
                'Không thể xóa sản phẩm này vì dữ liệu đang được sử dụng '
                'hoặc có liên kết với đơn hàng.'
            )

        return redirect('products:admin_product_list')

    context = {
        'product': product,
    }

    return render(
        request,
        'pages/admin_product_confirm_delete.html',
        context
    )
