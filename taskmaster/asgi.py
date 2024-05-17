"""
ASGI config for abinci project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from taskmaster.wsgi import *


asgi_app = get_asgi_application()

import taskmanager.urls
from taskmanager.middlewares import JWTAuthMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager.settings")
django.setup()
application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": AllowedHostsOriginValidator(
            JWTAuthMiddleware(URLRouter(taskmanager.urls.ws_urlpatterns))
        ),
    }
)
