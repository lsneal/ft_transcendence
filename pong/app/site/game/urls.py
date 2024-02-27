
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns
from .views import JoinGameView, GetGameView, UserIdGameView, CreateTournamentView, HealthView

urlpatterns = [
    #path('api/pong/pong/', views.pong),
    path('api/pong/UserIdGameView', UserIdGameView.as_view()),
    path('api/pong/joinGame/', JoinGameView.as_view()),
    path('api/pong/getGame/<int:pk>/', GetGameView.as_view()),
    path('api/pong/tournament', CreateTournamentView.as_view()),
    
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('health/', HealthView.as_view()),
]