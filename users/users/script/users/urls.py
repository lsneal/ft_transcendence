from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/user/', UserView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('2fa/', LoginA2F.as_view(), name='login_2fa'),
    path('qr_code/', views.qr_code, name='qr_code'),
    path('activate2fa/', ActivateA2F.as_view(), name='activate2fa'),
]
