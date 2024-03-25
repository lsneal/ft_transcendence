from django.urls import path, include
from .views import  PlayerRanking, ConnectUserStats



urlpatterns = [
    path('api/dashboard/player-ranking/', PlayerRanking.as_view()),
    path('api/dashboard/connectUser/', ConnectUserStats.as_view()), 
    path('health/', HealthView.as_view()),
]

