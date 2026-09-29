# Website Bán Hàng Phong Cách Con Cưng (Django + Supabase)

Dự án website thương mại điện tử chuyên ngành Mẹ & Bé, mô phỏng giao diện, chức năng và bố cục của **Concung.com**.

## Bảng Màu Giao Diện (Tone & Design System)
* **Màu chủ đạo (Primary Accent)**: `#FF82AB` (Hồng pastel ngọt ngào cho Mẹ & Bé)
* **Màu nền trang (Background)**: `#FFE7BA` (Vàng kem ấm áp, dễ chịu)
* **Các cột & khối chức năng (Cards & Columns)**: `#FFFFFF` (Trắng tinh tế với bóng đổ mượt)

## Các Tính Năng Cốt Lõi
1. **Header Đa Tầng**:
   * Hotline CSKH `1800 6609` (Gọi miễn phí).
   * Tra cứu hệ thống `1,164 siêu thị` trên toàn quốc.
   * Thanh tìm kiếm thông minh có popup **Tìm kiếm bằng hình ảnh** & gợi ý từ khóa.
   * Badge giỏ hàng và chuông thông báo ưu đãi.
2. **Sticky Category Mega Menu**:
   * Thanh danh mục bên trái cố định khi cuộn.
   * Hover hiển thị Flyout Mega Menu gồm phân loại con & lưới logo thương hiệu.
3. **Flash Sale Realtime**:
   * Đồng hồ đếm ngược giờ:phút:giây (`HH:MM:SS`).
   * Thanh tiến độ đã bán hàng.
4. **Trang Chi Tiết & Giỏ Hàng**:
   * Thư viện ảnh, quà tặng kèm, cam kết giao siêu tốc 1h.
   * Cập nhật giỏ hàng tức thì bằng JavaScript.
   * Form đặt hàng giao 1h và thanh toán linh hoạt.

## Hướng Dẫn Chạy Dự Án

### 1. Cài đặt thư viện:
```bash
pip install -r requirements.txt
```

### 2. Cấu hình kết nối Supabase (Tùy chọn):
Tạo file `.env` từ `.env.example` và điền chuỗi kết nối Supabase Postgres:
```env
DATABASE_URL=postgresql://postgres.xxxxxx:YOUR_PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres?sslmode=require
```
*(Nếu không điền, hệ thống sẽ tự động dùng SQLite offline để bạn chạy ngay lập tức)*.

### 3. Migrate và Khởi tạo Dữ liệu Mẫu:
```bash
python manage.py makemigrations
python manage.py migrate
python seed_data.py
```

### 4. Tạo tài khoản Quản trị (Admin):
```bash
python manage.py createsuperuser
```

### 5. Khởi chạy Server:
```bash
python manage.py runserver
```
Truy cập:
* Giao diện người dùng: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
* Trang quản trị Django Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
