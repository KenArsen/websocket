from django.urls import re_path, path
from chat.api.consumers.group_consumer import GroupChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/group/(?P<group_id>\d+)/$', GroupChatConsumer.as_asgi()),
]
