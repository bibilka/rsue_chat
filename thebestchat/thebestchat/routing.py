from .wsgi import *  # add this line to top of your code
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.core.asgi import get_asgi_application
import os
from pathlib import Path

if (os.environ.get('RSUECHAT_PROD_ENV', 'False') == 'True'):
    import thebestchat.chat.routing as routing
    application = ProtocolTypeRouter({
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })
else:
    import chat.routing as routing
    application = ProtocolTypeRouter({
        'websocket': AuthMiddlewareStack(
            URLRouter(
                routing.websocket_urlpatterns
            )
        ),
    })