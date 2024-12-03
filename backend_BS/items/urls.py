from django.urls import path,re_path
from items import views

urlpatterns = [
    re_path('crawl/', views.fetch_taobao_items),
    re_path('search/', views.search_items),
    ]