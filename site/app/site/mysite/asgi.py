"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
import uvicorn
import os
import django
from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.routing import get_default_application
 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()


myapp = get_asgi_application()

import app.routing
application = ProtocolTypeRouter({
    "http": myapp,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns
        )
    ),
})
    
if __name__ == "__main__":
    uvicorn.run("server:app")