import json
from random import randint
from asyncio import sleep

from channels.generic.websocket import AsyncWebsocketConsumer


class Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        for i in range(1000):
            await self.send(json.dumps({'message': randint(1, 100)}))
            await sleep(1)
