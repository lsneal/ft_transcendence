from django.urls import path, include
from .views import RegisterView, LoginView, UserView, LogoutView, HealthView, LoginA2F, ActivateA2F, A2FView, DisableA2F
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('health/', HealthView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/user/', UserView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/2fa/', LoginA2F.as_view(), name='login_2fa'),
    path('api/activate2fa/', ActivateA2F.as_view(), name='activate2fa'),
    path('api/disable2fa/', DisableA2F.as_view(), name='disable2fa'),
    path('api/a2fview/', A2FView.as_view(), name='a2fview'),
]
