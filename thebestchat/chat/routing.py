from django.urls import path
from dotenv import load_dotenv
from . import consumers
import os

load_dotenv()
if (os.getenv("PRODUCTION_ENV") == 'True'):
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
    ]
else:
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer),
    ]