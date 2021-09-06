from rest_framework import generics
from users.permissions import IsAuthenticated
from notifications.serializers import NotificationSerializer
from notifications.models import Notification

class UserNotificationView(generics.ListAPIView):
    '''fields = ('id', 'seen', 'recipient', 'log')'''
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)