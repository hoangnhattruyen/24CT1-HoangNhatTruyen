from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('api/messages/', views.send_or_get_messages, name='api_messages'),
]
