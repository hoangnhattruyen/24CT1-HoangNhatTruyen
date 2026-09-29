from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import ChatSession, ChatMessage
from .ai_advisor import ConCungAIAdvisor
from apps.accounts.models import StaffShift

def send_or_get_messages(request):
    """
    API Chat 24/7 thông minh:
    - Hỗ trợ chuyển đổi Chế độ AI (Phản hồi tức thì 24/7) và Nhân viên CSKH.
    - Tự động gọi AI Advisor khi ở chế độ AI hoặc khi không có nhân viên trực.
    """
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
        
    name = request.user.first_name or request.user.username if request.user.is_authenticated else "Khách mua sắm"
    
    if request.user.is_authenticated:
        session, _ = ChatSession.objects.get_or_create(customer=request.user, is_resolved=False, defaults={'customer_name': name})
    else:
        session, _ = ChatSession.objects.get_or_create(session_key=session_key, is_resolved=False, defaults={'customer_name': name})
        
    # Xử lý đổi chế độ chat (AI <-> Staff)
    switch_mode = request.POST.get('switch_mode')
    if switch_mode in ['AI', 'STAFF']:
        session.chat_mode = switch_mode
        session.save()
        
        mode_text = "🤖 Đã chuyển sang **Trợ lý AI Mẹ & Bé 24/7**. Em luôn sẵn sàng tư vấn dinh dưỡng và chọn sản phẩm ngay lập tức ạ!" if switch_mode == 'AI' else "👩‍💼 Đã kết nối với **Nhân viên CSKH**. Chuyên viên tư vấn sẽ hỗ trợ ba mẹ ngay ạ!"
        ChatMessage.objects.create(
            session=session,
            sender_name="Hệ Thống Con Cưng",
            is_staff=True,
            is_ai=(switch_mode == 'AI'),
            message=mode_text
        )
        return JsonResponse({'success': True, 'mode': session.chat_mode})

    # Xử lý gửi tin nhắn
    if request.method == 'POST':
        msg_text = request.POST.get('message', '').strip()
        if msg_text:
            # 1. Lưu tin nhắn của khách
            ChatMessage.objects.create(
                session=session,
                sender=request.user if request.user.is_authenticated else None,
                sender_name=name,
                is_staff=False,
                is_ai=False,
                message=msg_text
            )
            session.save()

            # 2. Xử lý phản hồi tự động
            # Kiểm tra xem có nhân viên nào đang trong ca trực không
            active_staff_count = StaffShift.objects.filter(check_out__isnull=True).count()
            
            if session.chat_mode == 'AI' or active_staff_count == 0:
                # Gọi AI tư vấn ngay lập tức
                ai_result = ConCungAIAdvisor.get_ai_response(msg_text)
                
                ai_prefix = "" if session.chat_mode == 'AI' else "(Hiện tại ngoài giờ trực của chuyên viên, AI Con Cưng xin phép hỗ trợ ba mẹ 24/7 ngay ạ):\n\n"
                
                ChatMessage.objects.create(
                    session=session,
                    sender_name="🤖 Con Cưng AI (Tư vấn 24/7)",
                    is_staff=True,
                    is_ai=True,
                    message=ai_prefix + ai_result['text'],
                    suggested_products_json=ai_result['suggested_products']
                )

            return JsonResponse({'success': True})
            
    # GET: Trả về toàn bộ lịch sử tin nhắn
    msgs = session.messages.all()
    data = []
    for m in msgs:
        data.append({
            'sender': m.sender_name,
            'is_staff': m.is_staff,
            'is_ai': m.is_ai,
            'text': m.message,
            'products': m.suggested_products_json or [],
            'time': m.created_at.strftime('%H:%M')
        })
    return JsonResponse({
        'mode': session.chat_mode,
        'messages': data
    })
