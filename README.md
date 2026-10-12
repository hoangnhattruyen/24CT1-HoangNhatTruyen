# Website Bán Hàng Phong Cách Con Cưng (Django + Supabase)

Dự án website thương mại điện tử chuyên ngành Mẹ & Bé, mô phỏng giao diện, chức năng và bố cục của **Concung.com**.

## Kiến Trúc Hệ Thống & Cơ Sở Dữ Liệu (System Architecture)
* **Frontend Layer**: Django Templates, HTML5, CSS3, JavaScript.
* **Backend Layer**: Django Web Framework (Python).
* **Database Layer**: **Supabase (PostgreSQL Cloud Database)**
  - Toàn bộ cơ sở dữ liệu của ứng dụng được lưu trữ và xử lý trực tiếp trên nền tảng đám mây **Supabase PostgreSQL**.
  - Các phân hệ dữ liệu chính trên **Supabase**:
    - **Supabase Accounts & Auth**: Quản lý người dùng, phân quyền, số điện thoại (`auth_user`, `accounts_userprofile`, `accounts_address`).
    - **Supabase Product Catalog**: Quản lý danh mục, thương hiệu, sản phẩm (`products_product`, `products_category`, `products_brand`).
    - **Supabase Orders & Cart**: Quản lý giỏ hàng và đơn hàng (`orders_cart`, `orders_order`, `orders_orderitem`).
    - **Supabase Promotions**: Quản lý chương trình Flash Sale và Voucher (`promotions_flashsale`, `promotions_voucher`).
    - **Supabase Store Operations**: Quản lý chuỗi siêu thị (`stores_storelocation`).
    - **Supabase Chat Support**: Quản lý phiên chat tư vấn trực tuyến (`chat_chatsession`, `chat_chatmessage`).


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
