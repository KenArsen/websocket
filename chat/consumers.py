# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# from django.contrib.auth.models import AnonymousUser
# from .models import Conversation, Message
# from .serializers import MessageSerializer
# from user.models import User
# from channels.db import database_sync_to_async
#
#
# class ChatConsumer(AsyncJsonWebsocketConsumer):
#     """
#     This consumer is used to show user's online status,
#     and send notifications.
#     """
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, kwargs)
#         self.user = None
#         self.conversation_name = None
#         self.conversation = None
#
#     async def connect(self):
#         print('Connected!')
#         self.user = self.scope['user']
#
#         # Проверяем, аутентифицирован ли пользователь
#         if self.user is None or isinstance(self.user, AnonymousUser):
#             await self.close()
#             return
#
#         await self.accept()
#         self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
#         self.conversation, created = await database_sync_to_async(Conversation.objects.get_or_create)(
#             name=self.conversation_name)
#         await self.channel_layer.group_add(
#             self.conversation_name,
#             self.channel_name,
#         )
#         messages = await database_sync_to_async(
#             lambda: list(self.conversation.messages.all().order_by("-timestamp")[0:50]))()
#         await self.send_json({
#             "type": "last_50_messages",
#             "messages": MessageSerializer(messages, many=True).data,
#         })
#
#     async def disconnect(self, code):
#         if self.conversation_name:
#             await self.channel_layer.group_discard(
#                 self.conversation_name,
#                 self.channel_name,
#             )
#         print("Disconnected!")
#         return await super().disconnect(code)
#
#     async def receive_json(self, content, **kwargs):
#         # Проверяем, аутентифицирован ли пользователь
#         if self.user is None or isinstance(self.user, AnonymousUser):
#             await self.close()
#             return
#
#         message_type = content.get("type")
#         if message_type == "chat_message":
#             receiver = await self.get_receiver()
#             message = await database_sync_to_async(Message.objects.create)(
#                 from_user=self.user,
#                 to_user=receiver,
#                 content=content["message"],
#                 conversation=self.conversation
#             )
#             await self.channel_layer.group_send(
#                 self.conversation_name,
#                 {
#                     "type": "chat_message_echo",
#                     "name": self.user.first_name,
#                     "message": MessageSerializer(message).data,
#                 },
#             )
#         return await super().receive_json(content, **kwargs)
#
#     async def chat_message_echo(self, event):
#         await self.send_json(event)
#
#     async def get_receiver(self):
#         usernames = self.conversation_name.split("__")
#         for username in usernames:
#             if username != self.user.first_name:
#                 return await database_sync_to_async(User.objects.get)(first_name=username)
