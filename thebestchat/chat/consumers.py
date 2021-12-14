import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Message, Profile, Chat
from django.utils import formats
from datetime import datetime

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chatId = self.scope['url_route']['kwargs']['chat_id']
        self.chatName = 'chat_' + self.chatId

        # Join room group
        await self.channel_layer.group_add(
            self.chatName,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chatName,
            self.channel_name
        )

    @database_sync_to_async
    def new_message(self, message, profile, chat):
        message = Message.objects.create(text=message)
        message.profile = Profile.objects.get(id=profile)
        message.chat = Chat.objects.get(id=chat)
        message.save()

    @database_sync_to_async
    def get_profile_avatar(self, profile):
        return Profile.objects.get(pk=profile).avatar

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        profile = text_data_json['profileId']
        chat = text_data_json['chatId']

        if (len(message) > 0):
            await self.new_message(message=message, profile=profile, chat=chat)

            avatar = await self.get_profile_avatar(profile)

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

    async def chat_message(self, event):
        message = event['message']
        profile = event['profile']

        await self.send(text_data=json.dumps({
            'message': message,
            'profile': profile
        }, ensure_ascii=False, default=str))