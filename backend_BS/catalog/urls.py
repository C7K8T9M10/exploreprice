from django.urls import path,re_path
from catalog import views

urlpatterns = [
  re_path('register/', views.register),
  re_path('login/', views.user_login),
]
