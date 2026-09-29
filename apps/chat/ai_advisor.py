import re
from apps.products.models import Product, Category

class ConCungAIAdvisor:
    """
    Hệ thống AI Tư vấn Sản phẩm Mẹ & Bé 24/7:
    - Phân tích độ tuổi, cân nặng của bé, tình trạng tiêu hóa/dinh dưỡng, nhu cầu của mẹ.
    - Tìm kiếm và gợi ý các sản phẩm chính xác nhất từ cơ sở dữ liệu của cửa hàng.
    - Trả lời thân thiện, chuẩn kiến thức y khoa chăm sóc Mẹ & Bé.
    """

    KNOWLEDGE_BASE = {
        'sua_tieu_hoa': {
            'keywords': ['táo bón', 'tiêu hóa', 'mát', 'nóng trong', 'dễ tiêu', 'nôn trớ', 'đầy hơi'],
            'advice': 'Đối với các bé có cơ địa nóng, dễ bị táo bón hoặc đầy hơi, ba mẹ nên ưu tiên các dòng sữa có thành phần đạm mềm, bổ sung Synbiotics (chất xơ GOS/FOS và lợi khuẩn Probiotics) như **Meiji** (dòng sữa rau của Nhật) hoặc **Aptamil Profutura** (chứa men vi sinh tự nhiên tương tự sữa mẹ).',
            'product_query': 'sua'
        },
        'sua_tang_can': {
            'keywords': ['tăng cân', 'nhẹ cân', 'còi xương', 'suy dinh dưỡng', 'chậm lớn', 'biếng ăn'],
            'advice': 'Để hỗ trợ bé bắt kịp đà tăng trưởng và tăng cân chuẩn khoa học, ba mẹ nên chọn sữa giàu năng lượng chuẩn, hàm lượng đạm chất lượng cao kết hợp MCT dễ hấp thu và Kẽm, Lysine kích thích ngon miệng.',
            'product_query': 'sua'
        },
        'ta_size': {
            'keywords': ['size tã', 'chọn size', 'bỉm', 'tã dán', 'tã quần', 'tràn bỉm', 'hằn đùi', 'hăm tã'],
            'advice': '💡 **Bảng tư vấn chọn size tã chuẩn theo cân nặng bé:**\n• **Size NB (Sơ sinh)**: Dành cho bé dưới 5kg\n• **Size S**: Dành cho bé 4 - 8kg\n• **Size M**: Dành cho bé 6 - 11kg\n• **Size L**: Dành cho bé 9 - 14kg\n• **Size XL**: Dành cho bé 12 - 17kg\n• **Size XXL**: Dành cho bé trên 15kg\nNếu bé có đùi/bụng trộm vía bụ bẫm, ba mẹ nên chủ động tăng lên 1 size và ưu tiên dòng tã có vách chống tràn & đệm mây êm ái như **Bobby** hoặc **Huggies Skin Perfect** nhé!',
            'product_query': 'ta'
        },
        'binh_sua': {
            'keywords': ['bình sữa', 'chống sặc', 'núm ti', 'đầy hơi', 'ppsu', 'kháng khuẩn', 'bình pigeon'],
            'advice': 'Khi chọn bình sữa cho bé, chất liệu **nhựa PPSU y tế cao cấp** chịu nhiệt tới 180°C và **núm ti silicone siêu mềm** có van thông khí AVS chống sặc, chống đầy hơi là lựa chọn an toàn số 1. Dòng bình **Pigeon PPSU Plus Nhật Bản** đang là dòng sản phẩm được các mẹ bỉm sữa tin dùng nhất.',
            'product_query': 'binh'
        },
        'do_so_sinh': {
            'keywords': ['sơ sinh', 'đi sinh', 'giỏ đồ', 'chuẩn bị', 'đồ bầu', 'mới sinh'],
            'advice': '🤱 **Danh sách đồ thiết yếu cần chuẩn bị cho Mẹ & Bé:**\n1. Tã dán sơ sinh Size NB (1-2 bịch).\n2. Sữa bột số 0 & Bình sữa chống sặc PPSU.\n3. Khăn ướt kháng khuẩn, khăn sữa cotton organic.\n4. Quần áo cài chéo Animo cotton 100% mềm mại.\n5. Nước giặt xả chuyên dụng và sữa tắm gội dịu lành.',
            'product_query': 'so-sinh'
        }
    }

    @classmethod
    def get_ai_response(cls, user_message):
        msg_lower = user_message.lower()
        matched_advice = None
        target_keyword = None

        for category_key, data in cls.KNOWLEDGE_BASE.items():
            for kw in data['keywords']:
                if kw in msg_lower:
                    matched_advice = data['advice']
                    target_keyword = data['product_query']
                    break
            if matched_advice:
                break

        # Nếu không khớp nhóm từ khóa cụ thể, dùng câu trả lời tổng quan thông minh
        if not matched_advice:
            matched_advice = (
                f"Dạ Con Cưng AI xin ghi nhận câu hỏi của ba mẹ về: \"{user_message}\".\n"
                "Tất cả sản phẩm tại Con Cưng đều là hàng chính hãng 100%, được kiểm định chất lượng nghiêm ngặt và hỗ trợ giao siêu tốc 1h tận nhà. Dưới đây là các sản phẩm nổi bật phù hợp với nhu cầu của ba mẹ ạ:"
            )

        # Trích xuất sản phẩm liên quan từ CSDL
        suggested_products = []
        products = Product.objects.filter(is_active=True)

        if target_keyword == 'sua' or 'sữa' in msg_lower:
            products = products.filter(category__slug__icontains='sua')[:3]
        elif target_keyword == 'ta' or 'tã' in msg_lower or 'bỉm' in msg_lower:
            products = products.filter(category__slug__icontains='ta')[:3]
        elif target_keyword == 'binh' or 'bình' in msg_lower:
            products = products.filter(category__slug__icontains='binh')[:3]
        else:
            products = products.filter(is_featured=True)[:3]

        for p in products:
            suggested_products.append({
                'id': p.id,
                'name': p.name,
                'price': f"{p.price:,.0f}₫".replace(',', '.'),
                'old_price': f"{p.original_price:,.0f}₫".replace(',', '.') if p.original_price else '',
                'image': p.display_image,
                'url': f"/product/{p.slug}/",
                'fast_1h': p.is_fast_delivery_1h,
                'gift': p.gift_description or ''
            })

        return {
            'text': matched_advice,
            'suggested_products': suggested_products
        }
