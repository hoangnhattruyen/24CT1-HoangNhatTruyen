from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('product/<slug:slug>/review/', views.add_review_view, name='add_review'),
    path('best-sellers/', views.best_sellers_view, name='best_sellers'),
    path('top-rated/', views.top_rated_view, name='top_rated'),
    path('api/search/', views.search_api_view, name='search_api'),
]
