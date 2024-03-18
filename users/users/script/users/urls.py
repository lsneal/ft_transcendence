from django.urls import path, include
from .views import RegisterView, LoginView, Login42View, UserView, LogoutView, HealthView, LoginA2F, ActivateA2F
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('health/', HealthView.as_view()),
    path('api/users/register/', RegisterView.as_view()),
    path('api/users/login/', LoginView.as_view()),
    path('api/users/login42/', Login42View.as_view()),
    path('api/users/user/', UserView.as_view()),
    path('api/users/logout/', LogoutView.as_view()),
    path('api/users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/2fa/', LoginA2F.as_view(), name='login_2fa'),
    path('api/users/activate2fa/', ActivateA2F.as_view(), name='activate2fa'),
]
