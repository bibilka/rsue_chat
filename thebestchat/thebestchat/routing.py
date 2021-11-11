from .wsgi import *  # add this line to top of your code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing as routing
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv
import os

load_dotenv()

if (os.getenv("PRODUCTION_ENV") == 'True'):
    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })
else:
    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })