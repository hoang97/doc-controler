import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from notifications.models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    # Connect to Websocket
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.user_group = f'user_{self.user_id}'

        await self.channel_layer.group_add(
            self.user_group, 
            self.channel_name
        )
        await self.accept()

    # Disconnect from Websocket
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_group, 
            self.channel_name
        )

    @database_sync_to_async
    def mark_notification_seen(self, notification_id):
        Notification.objects.filter(id = notification_id).update(seen=True)

    # User have seen a notification
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_id = text_data_json['notification_id']
        print('User seen notification ', notification_id)
        await self.channel_layer.group_send(
            self.user_group,
            {
                'type': 'notify.user',
                'message_type': 'seen',
                'notification_id': notification_id,
            }
        )
        await self.mark_notification_seen(notification_id)

    # Send notification via Websocket
    async def notify_user(self, event):
        await self.send(text_data=json.dumps(event))
