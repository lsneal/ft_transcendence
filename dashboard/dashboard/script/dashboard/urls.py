from django.urls import path, include
from .views import UserStats, PlayerRanking, ConnectUserStats
#from . import views *



urlpatterns = [
    #path('health/', HealthView.as_view()),
   path('api/dashboard/user-stats/', UserStats.as_view()),  
    path('api/dashboard/player-ranking/', PlayerRanking.as_view()),
    path('api/dashboard/connectUser/', ConnectUserStats.as_view()),  
]

