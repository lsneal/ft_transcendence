from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    #path('login/', views.user_login, name='user_login'),
    #path('register/', views.register, name='register'),
    #path('qr_code/', views.qr_code, name='qr_code'),
    path('register/', register.as_view(), name='register')
]