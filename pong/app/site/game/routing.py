from django.urls import re_path, path
from . import GameConsumers
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    path('api/pong/ws/<str:game_name>', GameConsumers.GameConsumer.as_asgi())
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})