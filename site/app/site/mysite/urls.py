"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from app import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.views import JoinGameView, GetGameView, UserIdGameView, CreateTournamentView

urlpatterns = [
    #path('api/pong/pong/', views.pong),
    path('api/pong/UserIdGameView', UserIdGameView.as_view()),
    path('api/pong/joinGame/', JoinGameView.as_view()),
    path('api/pong/getGame/<int:pk>/', GetGameView.as_view()),
    path('api/pong/tournament', CreateTournamentView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)