from django.urls import path
from . import views

app_name = 'stores'

urlpatterns = [
    path('tim-sieu-thi/', views.store_locator_view, name='store_locator'),
]
