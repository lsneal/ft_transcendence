from django.urls import path, include
from .views import UserStats, PlayerRanking
#from . import views *



urlpatterns = [
    #path('health/', HealthView.as_view()),
   path('api/dashboard/user-stats/', UserStats.as_view(), name='user-stats'),  
    path('api/dashboard/player-ranking/', PlayerRanking.as_view(), name='player-ranking'),  
]

