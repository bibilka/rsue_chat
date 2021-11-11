from django.urls import path
from . import consumers
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

if (config['Settings']['PRODUCTION_ENV'] == 'True'):
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
    ]
else:
    websocket_urlpatterns = [
        path('ws/<str:chat_id>/', consumers.ChatConsumer),
    ]