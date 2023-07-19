"""
ASGI config for hororok project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import os
from channels.routing import ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import chat.routing
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hororok.settings')
application = ProtocolTypeRouter({
    "http" : get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack( 
            URLRouter(
                chat.routing.websocket_urlpatterns
                )
        )
    )
})
