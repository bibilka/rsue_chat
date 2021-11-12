from .wsgi import *  # add this line to top of your code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing as routing
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})