# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
#
# from user.models import User
# from .models import Chat, Message
# from asgiref.sync import sync_to_async
#
#
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.chat_type = self.scope['url_route']['kwargs']['chat_type']
#         self.chat_id = self.scope['url_route']['kwargs']['chat_id']
#
#         if self.chat_type == 'group':
#             self.room_group_name = f'group_chat_{self.chat_id}'
#         else:
#             self.room_group_name = f'private_chat_{self.chat_id}'
#
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
#
#         await self.accept()
#
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )
#
#     async def receive(self, text_data=None, bytes_data=None):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         user_id = text_data_json['user']
#
#         user = User.objects.get(pk=user_id)
#         chat = await self.get_chat(user=user)
#         if chat:
#             Message.objects.create(chat=chat, sender=user, content=message)
#
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': message,
#                 'sender': user.first_name
#             }
#         )
#
#     async def chat_message(self, event):
#         message = event['message']
#         sender = event['sender']
#
#         await self.send(text_data=json.dumps({
#             'message': message,
#             'sender': sender
#         }))
#
#     async def get_chat(self, user):
#         if self.chat_type == 'group':
#             return await self.retrieve_chat(Chat.objects.filter(id=self.chat_id))
#         else:
#             return await self.retrieve_chat(Chat.objects.filter(id=self.chat_id, members=user))
#
#     async def retrieve_chat(self, queryset):
#         return await sync_to_async(queryset.first)()


from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from .models import Conversation, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_name = None
        self.user = None

    async def connect(self):
        print('Connected!')
        self.user = self.scope['user']
        print(self.user.email)

        # Проверяем, аутентифицирован ли пользователь
        if self.user is None or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.room_name = "home"
        await self.accept()
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        await self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    async def disconnect(self, code):
        if self.room_name:
            await self.channel_layer.group_discard(
                self.room_name,
                self.channel_name,
            )
        print("Disconnected!")
        return super().disconnect(code)

    async def receive_json(self, content, **kwargs):
        # Проверяем, аутентифицирован ли пользователь
        if self.user is None or isinstance(self.user, AnonymousUser):
            await self.close()
            return

        message_type = content.get("type")
        if message_type == "chat_message":
            await self.channel_layer.group_send(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "name": content.get("name"),
                    "message": content.get("message"),
                }
            )
        print(content)
        return await super().receive_json(content, **kwargs)

    async def chat_message_echo(self, event):
        print(event)
        await self.send_json(event)
