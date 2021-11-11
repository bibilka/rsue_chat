from django.urls import path
from . import consumers
import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(str(Path(__file__).resolve().parent.parent) + '/config.ini')

if (config['Settings']['PRODUCTION_ENV'] == 'True'):
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
    ]
else:
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer),
    ]