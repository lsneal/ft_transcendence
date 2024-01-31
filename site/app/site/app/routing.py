from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path('ws/socket-server', consumers.ChatConsumer.as_asgi())
    #path('ws/<str:gameId>', consumers.ChatConsumer.as_asgi())
]