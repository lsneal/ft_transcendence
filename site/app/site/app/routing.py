from django.urls import re_path, path
from . import GameConsumers
from . import Matchmaking
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path('ws/<str:game_name>', GameConsumers.GameConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})