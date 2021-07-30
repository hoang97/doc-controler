import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from notifications.models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add (
            'notifications', self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'notifications', self.channel_name
        )

    @database_sync_to_async
    def mark_notification_seen(self, notification_id):
        Notification.objects.filter(id = notification_id).update(seen=True)

    async def receive(self, text_data):
        # User have seen a notification
        text_data_json = json.loads(text_data)
        notification_id = text_data_json['notification_id']

        await self.mark_notification_seen(notification_id)

    async def notify_user(self, event):
        # Notify user
        await self.send(text_data=json.dumps({
            'timestamp': event['timestamp'],
            'message': event['message'],
            'seen': event['seen'],
            'user_id': event['user_id'],
        }))
