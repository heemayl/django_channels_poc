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

        # When a websocket client connects, accept the connection
        # and get the data from `_get_content_async` as it comes
        # (and also send it to the client via the websocket)
        while True:
            content = await _get_content_async()

            # The `asyncio.sleep(0)` is needed for context-switching i.e.
            # to send the control back to the event loop so that it
            # can schedule some other async task in the meantime.

            # IMPORTANT: Without `asyncio.sleep(0)`, no other task can
            # be scheduled by the event loop so the `self.send` in the
            # following line won't even run i.e. no data could be sent
            # back via the websocket as it won't get a chance to run.

            # We can use any `sleep` value apart from 0 depending on
            # context but 0 is enough if our only intention is to do
            # context switching; so `asyncio.sleep(0)` is essentially
            # a trick when doing asyncio.
            await asyncio.sleep(0)

            await self.send(text_data=json.dumps({"message": content}))

    async def disconnect(self, close_code):
        pass
