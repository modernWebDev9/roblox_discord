# roblox/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from people import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roblox.settings')

# Get the Django ASGI application
django_asgi_app = get_asgi_application()

# Serve static files in development
if settings.DEBUG:
    from django.core.handlers.asgi import ASGIHandler
    from django.http import HttpResponse
    from django.contrib.staticfiles import finders
    
    class StaticFilesMiddleware:
        def __init__(self, app):
            self.app = app
        
        async def __call__(self, scope, receive, send):
            if scope['type'] == 'http' and scope['path'].startswith('/static/'):
                # Try to find the static file
                file_path = scope['path'][8:]  # Remove '/static/'
                found = finders.find(file_path)
                if found:
                    try:
                        with open(found[1], 'rb') as f:
                            content = f.read()
                        await send({
                            'type': 'http.response.start',
                            'status': 200,
                            'headers': [
                                [b'content-type', self._get_content_type(found[1])],
                            ],
                        })
                        await send({
                            'type': 'http.response.body',
                            'body': content,
                        })
                        return
                    except:
                        pass
            await self.app(scope, receive, send)
        
        def _get_content_type(self, file_path):
            if file_path.endswith('.css'):
                return b'text/css'
            elif file_path.endswith('.js'):
                return b'application/javascript'
            elif file_path.endswith('.png'):
                return b'image/png'
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                return b'image/jpeg'
            elif file_path.endswith('.webp'):
                return b'image/webp'
            elif file_path.endswith('.svg'):
                return b'image/svg+xml'
            else:
                return b'application/octet-stream'
    
    django_asgi_app = StaticFilesMiddleware(django_asgi_app)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter([
            path('ws/status/', consumers.StatusConsumer.as_asgi()),
        ])
    ),
})