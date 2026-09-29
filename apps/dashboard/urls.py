from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Staff portal
    path('staff/', views.staff_dashboard_view, name='staff_dashboard'),
    path('staff/order/<int:order_id>/update/', views.staff_update_order_status, name='staff_update_order'),
    path('staff/chat/<int:session_id>/', views.staff_chat_view, name='staff_chat'),
    
    # Admin portal & Quản lý tạo tài khoản
    path('admin-portal/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-portal/staff-manage/', views.admin_staff_manage_view, name='admin_staff_manage'),
    path('admin-portal/create-account/', views.admin_create_account_view, name='admin_create_account'),
    path('admin-portal/staff/<int:user_id>/toggle-status/', views.admin_toggle_staff_status, name='admin_toggle_staff_status'),
    path('admin-portal/review/<int:review_id>/toggle/', views.admin_toggle_review, name='admin_toggle_review'),
]
