from django.urls import path, include
from .views import UserStats, PlayerRanking, HealthView
#from . import views *



urlpatterns = [
    path('api/dashboard/user-stats/', UserStats.as_view()),  
    path('api/dashboard/player-ranking/', PlayerRanking.as_view()),
    path('health/', HealthView.as_view()),
]

