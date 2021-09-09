from rest_framework import generics
from users.permissions import IsAuthenticated
from notifications.serializers import LogSerializer, NotificationSerializer
from notifications.models import Notification, Log
from django.contrib.contenttypes.models import ContentType

class UserNotificationView(generics.ListAPIView):
    '''fields = ('id', 'seen', 'recipient', 'log')'''
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

class UserLogView(generics.ListAPIView):
    '''fields = ('id', 'timestamp', 'actor', 'target', 'verb', '__str__')'''
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Log.objects.filter(actor_id=self.request.user.id, actor_ct = ContentType.objects.get_for_model(self.request.user).id)