from rest_framework import serializers
from notifications.models import Log, Notification
from users.serializers import UserGeneralSerializer
from hsmt.models import XFile
from hsmt.serializers import XFileGeneralUpdateSerializer
from users.models import User
from users.serializers import UserGeneralSerializer
from todolist.models import Task, MiniTask

class LogActorSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserGeneralSerializer(value)
        elif isinstance(value, XFile):
            serializer = XFileGeneralUpdateSerializer(value)
        else:
            raise Exception('Unexpected type of actor object')
        return serializer.data

class LogTargetSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, User):
            serializer = UserGeneralSerializer(value)
        elif isinstance(value, XFile):
            serializer = XFileGeneralUpdateSerializer(value)
        else:
            raise Exception('Unexpected type of target object')
        return serializer.data

class LogSerializer(serializers.ModelSerializer):
    actor = LogActorSerializer(read_only=True)
    target = LogTargetSerializer(read_only=True)
    class Meta:
        model = Log
        fields = ('id', 'timestamp', 'actor', 'target', 'verb')

class NotificationSerializer(serializers.ModelSerializer):
    recipient = UserGeneralSerializer()
    log = LogSerializer()
    class Meta:
        model = Notification
        fields = ('id', 'seen', 'recipient', 'log')

