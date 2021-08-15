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
    def seen_notification(self, notification_id):
        Notification.objects.filter(id = notification_id).update(seen=True)

    @database_sync_to_async
    def delete_notification(self, notification_id):
        Notification.objects.get(id = notification_id).delete()

    # User have seen or deleted a notification
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action_type = text_data_json['action_type']
        notification_id = text_data_json['notification_id']
        if action_type == 'seen.notification':
            print('User seen notification ', notification_id)
            await self.channel_layer.group_send(
                self.user_group,
                {
                    'type': 'notify.user',
                    'message_type': 'seen',
                    'notification_id': notification_id,
                }
            )
            await self.seen_notification(notification_id)
        elif action_type == 'delete.notification':
            print('User deleted notification ', notification_id)
            await self.channel_layer.group_send(
                self.user_group,
                {
                    'type': 'notify.user',
                    'message_type': 'delete',
                    'notification_id': notification_id,
                }
            )
            await self.delete_notification(notification_id)

    # Send notification via Websocket
    async def notify_user(self, event):
        await self.send(text_data=json.dumps(event))
