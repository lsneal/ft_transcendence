from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, LoginA2F, qr_code, ActivateA2F
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('2fa/', LoginA2F.as_view(), name='login_2fa'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('activate2fa/', ActivateA2F.as_view(), name='activate2fa'),

]