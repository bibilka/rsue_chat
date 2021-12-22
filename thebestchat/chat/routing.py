from django.urls import path
from . import consumers

# урл паттерн для маршрутизации работы с веб-сокетами (для чата)
websocket_urlpatterns = [
    path('ws/<str:chat_id>/', consumers.ChatConsumer.as_asgi()),
]
