# roblox/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from people import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roblox.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/status/', consumers.StatusConsumer.as_asgi()),
        ])
    ),
})