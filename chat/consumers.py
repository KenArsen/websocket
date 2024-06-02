import json
from channels.generic.websocket import AsyncWebsocketConsumer

from user.models import User
from .models import Chat, Message
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_type = self.scope['url_route']['kwargs']['chat_type']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']

        if self.chat_type == 'group':
            self.room_group_name = f'group_chat_{self.chat_id}'
        else:
            self.room_group_name = f'private_chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = text_data_json['user']

        user = User.objects.get(pk=user_id)
        chat = await self.get_chat(user=user)
        if chat:
            Message.objects.create(chat=chat, sender=user, content=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': user.first_name
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender
        }))

    async def get_chat(self, user):
        if self.chat_type == 'group':
            return await self.retrieve_chat(Chat.objects.filter(id=self.chat_id))
        else:
            return await self.retrieve_chat(Chat.objects.filter(id=self.chat_id, members=user))

    async def retrieve_chat(self, queryset):
        return await sync_to_async(queryset.first)()
