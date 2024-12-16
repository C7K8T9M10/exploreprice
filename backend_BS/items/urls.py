from django.urls import path,re_path
from items import views

urlpatterns = [
    re_path('crawl/', views.fetch_taobao_items),
    re_path('search/', views.search_items),
    re_path('save/', views.save_item),
    re_path('rand/', views.random_items),
    re_path('getsav/', views.get_latest_saved_items),
    re_path('getprice/', views.get_price),
    re_path('getimg/', views.get_price_img),
    ]