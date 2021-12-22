import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Message, Profile, Chat
from django.utils import formats
from datetime import datetime

# Класс для обработки веб-сокетов. Бэкенд часть работы чата.
class ChatConsumer(AsyncWebsocketConsumer):

    # выполнение соединения
    async def connect(self):
        # получаем данные
        self.chatId = self.scope['url_route']['kwargs']['chat_id']
        self.chatName = 'chat_' + self.chatId

        # формируем новую группу (комнату) в channel слое
        await self.channel_layer.group_add(
            self.chatName,
            self.channel_name
        )

        # ожидаем принятия сообщения
        await self.accept()

    # метод для разрыва соединения
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chatName,
            self.channel_name
        )

    @database_sync_to_async
    def new_message(self, message, profile, chat):
        # создание нового сообщения, сохранение в базу данных
        message = Message.objects.create(text=message)
        message.profile = Profile.objects.get(id=profile)
        message.chat = Chat.objects.get(id=chat)
        message.save()

    @database_sync_to_async
    def get_profile_avatar(self, profile):
        # получение аватара профиля пользователя, который отправил сообщение
        return Profile.objects.get(pk=profile).avatar

    # метод обрабатывающий получение сообщения
    async def receive(self, text_data=None, bytes_data=None):
        # получаем данные
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        profile = text_data_json['profileId']
        chat = text_data_json['chatId']

        if (len(message) > 0):
            await self.new_message(message=message, profile=profile, chat=chat)

            avatar = await self.get_profile_avatar(profile)
            # отправляем сообщение в канал связи
            await self.channel_layer.group_send(
                self.chatName,
                {
                    'type': 'chat_message',
                    'message': {
                        'text': message,
                        'date': formats.date_format(datetime.now(), "DATETIME_FORMAT"),
                    },
                    'profile': {
                        'id': profile,
                        'avatar': avatar.url if avatar else '',
                    }
                }
            )

    # отправка сообщения
    async def chat_message(self, event):
        message = event['message']
        profile = event['profile']
        # отправляем сообщение в формате JSON
        await self.send(text_data=json.dumps({
            'message': message,
            'profile': profile
        }, ensure_ascii=False, default=str))