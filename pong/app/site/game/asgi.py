import uvicorn
import os
import django
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()


myapp = get_asgi_application()

import game.routing
application = ProtocolTypeRouter({
    "http": myapp,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            game.routing.websocket_urlpatterns
        )
    ),
})
    
if __name__ == "__main__":
    uvicorn.run("server:app")