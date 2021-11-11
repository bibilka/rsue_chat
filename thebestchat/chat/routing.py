from django.urls import path
from . import consumers
from pathlib import Path
import os

if (os.environ.get('RSUECHAT_PROD_ENV', 'False') == 'True'):
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
    ]
else:
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer),
    ]