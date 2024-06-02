import os

from channels.routing import ProtocolTypeRouter, URLRouter
from config.middleware import JWTAuthMiddleware
from django.core.asgi import get_asgi_application
from config.routing import websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': JWTAuthMiddleware(URLRouter(websocket_urlpatterns))
})
