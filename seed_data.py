import os
import django
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # Nạp biến DATABASE_URL từ file .env

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_core.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone
from apps.accounts.models import UserProfile, Address, StaffShift
from apps.products.models import Category, Brand, Product, ProductReview
from apps.promotions.models import Banner, FlashSale, FlashSaleItem, Voucher
from apps.stores.models import StoreLocation
from apps.orders.models import Order, OrderItem

print("Starting rich seed data without duplicates...")

# 1. Tạo Users: Admin, Staff, Customer
admin_user, _ = User.objects.get_or_create(username='admin', defaults={'first_name': 'Quản Trị Viên', 'is_superuser': True, 'is_staff': True})
admin_user.set_password('admin123')
admin_user.save()
UserProfile.objects.get_or_create(user=admin_user, defaults={'role': 'ADMIN', 'phone': '0901234567'})

staff1, _ = User.objects.get_or_create(username='nhanvien1', defaults={'first_name': 'Nguyễn Thị Thu (Tư Vấn)', 'is_staff': True})
staff1.set_password('staff123')
staff1.save()
UserProfile.objects.get_or_create(user=staff1, defaults={'role': 'STAFF', 'phone': '0907654321'})

cust1, _ = User.objects.get_or_create(username='mebong', defaults={'first_name': 'Mẹ Bống (Khách Hàng)'})
cust1.set_password('customer123')
cust1.save()
UserProfile.objects.get_or_create(user=cust1, defaults={'role': 'CUSTOMER', 'phone': '0988889999'})
Address.objects.get_or_create(
    user=cust1,
    receiver_name="Mẹ Bống",
    phone="0988889999",
    street_address="123 Lê Lợi, Phường Bến Thành",
    district="Quận 1",
    city="TP. Hồ Chí Minh",
    is_default=True
)

# 2. Tạo Ca trực mẫu cho Nhân viên
StaffShift.objects.get_or_create(
    staff=staff1,
    defaults={
        'orders_processed_count': 12,
        'revenue_generated': 6500000,
        'notes': 'Ca sáng trực tư vấn bình sữa và tã bỉm'
    }
)

# 3. Categories
categories_data = [
    {"name": "Sữa bột cao cấp", "slug": "sua-bot-cao-cap", "icon": "🍼", "order": 1},
    {"name": "Tã bỉm khuyến mãi", "slug": "ta-bim-khuyen-mai", "icon": "🧷", "order": 2},
    {"name": "Sữa tươi & Sữa chua", "slug": "sua-tuoi-sua-chua", "icon": "🥛", "order": 3},
    {"name": "Thực phẩm ăn dặm", "slug": "thuc-pham-an-dam", "icon": "🥣", "order": 4},
    {"name": "Bình sữa & Phụ kiện", "slug": "binh-sua-phu-kien", "icon": "🍼", "order": 5},
    {"name": "Thời trang bé trai", "slug": "thoi-trang-be-trai", "icon": "👕", "order": 6},
    {"name": "Thời trang bé gái", "slug": "thoi-trang-be-gai", "icon": "👗", "order": 7},
    {"name": "Đồ chơi & Học tập", "slug": "do-choi-hoc-tap", "icon": "🧸", "order": 8},
    {"name": "Chăm sóc mẹ & bé", "slug": "cham-soc-me-va-be", "icon": "🧴", "order": 9},
]
cats = {}
for c_data in categories_data:
    cat, _ = Category.objects.update_or_create(slug=c_data["slug"], defaults=c_data)
    cats[c_data["slug"]] = cat

# 4. Brands
brands_data = [
    {"name": "Meiji", "slug": "meiji", "is_featured": True},
    {"name": "Aptamil", "slug": "aptamil", "is_featured": True},
    {"name": "Enfagrow", "slug": "enfagrow", "is_featured": True},
    {"name": "Vinamilk", "slug": "vinamilk", "is_featured": True},
    {"name": "Huggies", "slug": "huggies", "is_featured": True},
    {"name": "Bobby", "slug": "bobby", "is_featured": True},
    {"name": "Pigeon", "slug": "pigeon", "is_featured": True},
    {"name": "Philips Avent", "slug": "philips-avent", "is_featured": True},
]
brands = {}
for b_data in brands_data:
    brand, _ = Brand.objects.get_or_create(slug=b_data["slug"], defaults=b_data)
    brand.categories.add(cats["sua-bot-cao-cap"], cats["ta-bim-khuyen-mai"])
    brands[b_data["slug"]] = brand

# 5. Danh Sách 12 Sản Phẩm Đa Dạng Không Trùng Lặp
products_data = [
    # --- Nhóm Bán Chạy (Best Sellers) ---
    {
        "name": "Sữa bột Meiji số 0 (0-12 tháng) 800g Nhập khẩu Nhật Bản",
        "slug": "sua-meiji-so-0-800g",
        "sku": "MEIJI-0-800",
        "category": cats["sua-bot-cao-cap"],
        "brand": brands["meiji"],
        "price": 529000,
        "original_price": 585000,
        "stock": 45,
        "sold_count": 890,
        "rating": 4.9,
        "review_count": 128,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr7wEnDwMtX0PkwuU361iDjMEoo44WPEmoU-i9Hf6XBOZjBLAc3-nRDiA&s=10",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng gấu bông cao cấp",
        "is_featured": True,
        "origin": "Nhật Bản",
        "age_group": "0_1"
    },
    {
        "name": "Tã quần Bobby Lõi nén thần kỳ Size L (9-14kg) 68 miếng",
        "slug": "ta-quan-bobby-size-l-68",
        "sku": "BOBBY-PANT-L68",
        "category": cats["ta-bim-khuyen-mai"],
        "brand": brands["bobby"],
        "price": 315000,
        "original_price": 389000,
        "stock": 80,
        "sold_count": 750,
        "rating": 4.8,
        "review_count": 95,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCuYg6R8wIT18oycBqFq0fAPr5LCFM7OENwYgQCGljUQ&s=10",
        "is_fast_delivery_1h": True,
        "gift_description": "Giảm ngay 40k khi mua từ 2 gói",
        "is_featured": True,
        "origin": "Việt Nam",
        "age_group": "1_2"
    },
    {
        "name": "Sữa Enfagrow A+ NeuroPro Số 3 Vị Không Đường 830g",
        "slug": "sua-enfagrow-a-neuropro-3-830g",
        "sku": "ENFA-NP3-830",
        "category": cats["sua-bot-cao-cap"],
        "brand": brands["enfagrow"],
        "price": 499000,
        "original_price": 560000,
        "stock": 35,
        "sold_count": 620,
        "rating": 4.9,
        "review_count": 82,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTv3c9WyYQjtvgFzJPtX9t3Jh5J9pJ_4lBP6xEGUjFCHA&s=10",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng bộ ghép hình phát triển trí tuệ",
        "is_featured": True,
        "origin": "Thái Lan",
        "age_group": "1_2"
    },
    {
        "name": "Tã dán Huggies Skin Perfect Tràm Trà Tự Nhiên Size NB 70 miếng",
        "slug": "ta-dan-huggies-skin-perfect-nb70",
        "sku": "HUG-SKIN-NB70",
        "category": cats["ta-bim-khuyen-mai"],
        "brand": brands["huggies"],
        "price": 245000,
        "original_price": 290000,
        "stock": 5,
        "sold_count": 540,
        "rating": 4.8,
        "review_count": 64,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3vht2VmZCrZgp7jMTlSWCuJAzgEZKVQwVWOUoUjH9nw&s=10",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng 1 gói khăn ướt kháng khuẩn",
        "is_featured": True,
        "origin": "Việt Nam",
        "age_group": "0_1"
    },

    # --- Nhóm Đánh Giá Cao 5 Sao (Top Rated) ---
    {
        "name": "Sữa bột Aptamil Profutura Úc Số 2 (6-12 tháng) 900g",
        "slug": "sua-aptamil-profutura-so-2-900g",
        "sku": "APTA-PRO-2",
        "category": cats["sua-bot-cao-cap"],
        "brand": brands["aptamil"],
        "price": 945000,
        "original_price": 1050000,
        "stock": 8,
        "sold_count": 310,
        "rating": 5.0,
        "review_count": 120,
        "main_image_url": "https://concung.com/2024/03/65922-108995-large_mobile/san-pham-dinh-duong-cong-thuc-voi-muc-dich-an-bo-sung-aptamil-profutura-2-premium-follow-on-formula-danh-cho-tre-tu-6-den-12-thang-tuoi.webp",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng Xe chòi chân khi mua 2 lon",
        "is_featured": True,
        "origin": "Úc",
        "age_group": "0_1"
    },
    {
        "name": "Bình sữa Pigeon PPSU Plus Cổ Rộng Kháng Khuẩn 240ml Nhật Bản",
        "slug": "binh-sua-pigeon-ppsu-240ml",
        "sku": "PIGEON-PPSU-240",
        "category": cats["binh-sua-phu-kien"],
        "brand": brands["pigeon"],
        "price": 385000,
        "original_price": 420000,
        "stock": 60,
        "sold_count": 480,
        "rating": 5.0,
        "review_count": 115,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjVR5REHrVKEL5h_bDx67Ll80rHTl7RfaL5y4w9MJW7cqHf8J7YDGZMdY&s=10",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng núm ti thay thế size M",
        "is_featured": True,
        "origin": "Nhật Bản",
        "age_group": "ALL"
    },
    {
        "name": "Bình sữa Philips Avent Natural Cổ Rộng Thủy Tinh 240ml",
        "slug": "binh-sua-avent-natural-240ml",
        "sku": "AVENT-NAT-240",
        "category": cats["binh-sua-phu-kien"],
        "brand": brands["philips-avent"],
        "price": 425000,
        "original_price": 490000,
        "stock": 25,
        "sold_count": 290,
        "rating": 5.0,
        "review_count": 78,
        "main_image_url": "https://down-vn.img.susercontent.com/file/vn-11134207-81ztc-moulbxjjwg0298",
        "is_fast_delivery_1h": True,
        "gift_description": "Van chống sặc thông minh",
        "is_featured": True,
        "origin": "Anh Quốc",
        "age_group": "ALL"
    },
    {
        "name": "Bột ăn dặm HiPP Organic Kiều Mạch Mận Tây 250g Nhập Khẩu Đức",
        "slug": "bot-an-dam-hipp-kieu-mach-250g",
        "sku": "HIPP-KIEUMACH-250",
        "category": cats["thuc-pham-an-dam"],
        "price": 145000,
        "original_price": 165000,
        "stock": 50,
        "sold_count": 340,
        "rating": 5.0,
        "review_count": 52,
        "main_image_url": "https://suachobeyeu.vn/application/upload/products/bot-an-dam-hipp-ngu-coc-voi-man-tay-5-grain-with-prune-hop-250g-1.jpg",
        "is_fast_delivery_1h": True,
        "gift_description": "Tặng thìa ăn dặm báo nóng",
        "is_featured": True,
        "origin": "Đức",
        "age_group": "0_1"
    },

    # --- Nhóm Hàng Mới Về (New Arrivals) ---
    {
        "name": "Bộ quần áo cotton organic cộc tay cài chéo Animo cho bé trai",
        "slug": "bo-quan-ao-cotton-animo-be-trai",
        "sku": "ANIMO-BOY-01",
        "category": cats["thoi-trang-be-trai"],
        "price": 149000,
        "original_price": 189000,
        "stock": 100,
        "sold_count": 45,
        "rating": 4.8,
        "review_count": 12,
        "main_image_url": "https://concung.com/2026/01/75394-134035-large_mobile/bo-polo-be-trai-ngan-animo-hn1225031-1-6y-trang-bien.webp",
        "is_fast_delivery_1h": True,
        "is_featured": False,
        "origin": "Việt Nam",
        "age_group": "0_1"
    },
    {
        "name": "Đầm xòe công chúa cotton mềm mại thêu hoa bé gái Animo",
        "slug": "dam-xoe-cong-chua-be-gai-animo",
        "sku": "ANIMO-GIRL-DRESS",
        "category": cats["thoi-trang-be-gai"],
        "price": 199000,
        "original_price": 249000,
        "stock": 40,
        "sold_count": 30,
        "rating": 4.9,
        "review_count": 15,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJD-kgTqI4J6XJkC8vhAQYn1mJIHbW3-0Zz2yIe61NlLN782Qk9qIGcoWF&s=10",
        "is_fast_delivery_1h": True,
        "is_featured": False,
        "origin": "Việt Nam",
        "age_group": "1_2"
    },
    {
        "name": "Thùng 48 hộp Sữa tươi tiệt trùng Vinamilk 100% Ít đường 180ml",
        "slug": "thung-sua-tuoi-vinamilk-it-duong-180ml",
        "sku": "VNM-FRESH-180",
        "category": cats["sua-tuoi-sua-chua"],
        "brand": brands["vinamilk"],
        "price": 389000,
        "original_price": 420000,
        "stock": 70,
        "sold_count": 180,
        "rating": 4.9,
        "review_count": 28,
        "main_image_url": "https://product.hstatic.net/1000288770/product/sua_tuoi_vinamilk_100_it_duong_thung_48_hop_x_180ml_ac89ae7d5d684fa6ba3e9f95ff0d83d9_master.jpg",
        "is_fast_delivery_1h": True,
        "is_featured": False,
        "origin": "Việt Nam",
        "age_group": "2_PLUS"
    },
    {
        "name": "Bộ đồ chơi xếp hình thông minh 100 chi tiết bằng gỗ tự nhiên",
        "slug": "bo-xep-hinh-go-thong-minh-100ct",
        "sku": "TOY-WOOD-100",
        "category": cats["do-choi-hoc-tap"],
        "price": 285000,
        "original_price": 350000,
        "stock": 20,
        "sold_count": 65,
        "rating": 5.0,
        "review_count": 22,
        "main_image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRgi8BYA5RZ4IuTSS2F5l4kt-m_kbMejtndViLzzUAuDLOZGub-Gsx4y6g&s=10",
        "is_fast_delivery_1h": True,
        "is_featured": False,
        "origin": "Việt Nam",
        "age_group": "2_PLUS"
    }
]

created_products = []
for p_data in products_data:
    p, created = Product.objects.get_or_create(sku=p_data["sku"], defaults=p_data)
    if not created:
        for k, v in p_data.items():
            setattr(p, k, v)
        p.save()
    created_products.append(p)

# 6. Đánh giá & Feedback mẫu
for p in created_products:
    ProductReview.objects.get_or_create(
        product=p,
        user=cust1,
        defaults={
            'rating': int(p.rating),
            'comment': f"Sản phẩm {p.name} giao siêu nhanh trong 1h, bé nhà mình dùng rất ưng ý!",
            'is_approved': True
        }
    )

# 7. Vouchers
Voucher.objects.get_or_create(code="CONCUNG50K", defaults={'discount_amount': 50000, 'min_order_value': 300000, 'is_active': True})
Voucher.objects.get_or_create(code="FREESHIP", defaults={'discount_amount': 25000, 'min_order_value': 150000, 'is_active': True})

# 8. Flash Sale với 3 sản phẩm riêng biệt
flash_sale, _ = FlashSale.objects.get_or_create(
    title="GIÁ SỐC MỖI NGÀY - DEAL CHỚP NHOÁNG",
    defaults={
        "end_time": timezone.now() + timedelta(hours=6),
        "is_active": True
    }
)
flash_sale.items.all().delete()
for p in created_products[0:4]:
    FlashSaleItem.objects.create(
        flash_sale=flash_sale,
        product=p,
        flash_price=int(float(p.price) * 0.85),
        quantity_limit=50,
        quantity_sold=28
    )

# 9. Store Locations
stores_data = [
    {"name": "Siêu thị Con Cưng Nguyễn Du", "address": "66 Nguyễn Du, Phường Bến Nghé", "district": "Quận 1", "province": "TP. Hồ Chí Minh"},
    {"name": "Siêu thị Con Cưng Ba Tháng Hai", "address": "424-426 Ba Tháng Hai, Phường 12", "district": "Quận 10", "province": "TP. Hồ Chí Minh"},
    {"name": "Siêu thị Con Cưng Thái Hà", "address": "12 Thái Hà, Phường Trung Liệt", "district": "Quận Đống Đa", "province": "Hà Nội"},
]
for s_data in stores_data:
    StoreLocation.objects.get_or_create(name=s_data["name"], defaults=s_data)

# 10. Tạo các Đơn hàng phân bổ thời gian (Hôm nay, Tuần này, Tháng này)
# Xóa đơn cũ để nạp mới chuẩn số liệu
Order.objects.all().delete()

# Đơn 1: Hôm nay
o_today = Order.objects.create(
    order_code="CC083001",
    user=cust1,
    customer_name="Mẹ Bống",
    customer_phone="0988889999",
    shipping_address="123 Lê Lợi, Phường Bến Thành",
    district="Quận 1",
    city="TP. Hồ Chí Minh",
    shipping_method="FAST_1H",
    payment_method="COD",
    shipping_fee=0,
    total_amount=844000,
    status="SHIPPING"
)
OrderItem.objects.create(order=o_today, product=created_products[0], product_name=created_products[0].name, price=529000, quantity=1)
OrderItem.objects.create(order=o_today, product=created_products[1], product_name=created_products[1].name, price=315000, quantity=1)

# Đơn 2: 3 ngày trước (Tuần này)
o_week = Order.objects.create(
    order_code="CC082702",
    user=cust1,
    customer_name="Mẹ Thảo Vy",
    customer_phone="0911223344",
    shipping_address="45 Nguyễn Huệ",
    district="Quận 1",
    city="TP. Hồ Chí Minh",
    shipping_method="STANDARD",
    payment_method="VNPAY",
    shipping_fee=0,
    total_amount=1680000,
    status="DELIVERED"
)
o_week.created_at = timezone.now() - timedelta(days=3)
o_week.save()
OrderItem.objects.create(order=o_week, product=created_products[4], product_name=created_products[4].name, price=945000, quantity=1)
OrderItem.objects.create(order=o_week, product=created_products[6], product_name=created_products[6].name, price=425000, quantity=1)

# Đơn 3: 15 ngày trước (Tháng này)
o_month = Order.objects.create(
    order_code="CC081503",
    user=cust1,
    customer_name="Mẹ Bảo Châu",
    customer_phone="0977665544",
    shipping_address="88 Hai Bà Trưng",
    district="Quận 3",
    city="TP. Hồ Chí Minh",
    shipping_method="FAST_1H",
    payment_method="COD",
    shipping_fee=0,
    total_amount=4250000,
    status="DELIVERED"
)
o_month.created_at = timezone.now() - timedelta(days=15)
o_month.save()
OrderItem.objects.create(order=o_month, product=created_products[0], product_name=created_products[0].name, price=529000, quantity=4)

print("Seed data completed successfully with distinct products and revenue!")
