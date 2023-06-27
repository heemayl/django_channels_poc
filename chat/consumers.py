import asyncio
import json
import random
import time

from channels.generic.websocket import AsyncWebsocketConsumer


async def _get_content_async(*args, **kwargs):

    # Random blocking-sleep here to indicate some actual work being done
    random_value = random.random()
    time.sleep(random_value)

    return random_value


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        while True:
            content = await _get_content_async()
            await asyncio.sleep(0)
            await self.send(text_data=json.dumps({"message": content}))
