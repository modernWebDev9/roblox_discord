# people/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("status_group", self.channel_name)
        print(f"✅ WebSocket connected: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("status_group", self.channel_name)
        print(f"❌ WebSocket disconnected: {self.channel_name}")

    async def receive(self, text_data):
        pass

    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status'],
            'message': event['message'],
            'timestamp': event.get('timestamp', '')
        }))