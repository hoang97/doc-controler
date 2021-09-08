from rest_framework import serializers
from todolist.models import Task, MiniTask
from users.serializers import UserGeneralSerializer

class MiniTaskSerializer(serializers.ModelSerializer):
    users = UserGeneralSerializer(many=True)
    class Meta:
        model = MiniTask
        fields = ('id', 'title', 'content', 'status', 'deadline', 'start_at', 'updated_at', 'task', 'users')
        read_only_fields = ('id', 'updated_at', 'task', 'status')

class MiniTaskGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniTask
        fields = ('id', 'title', 'content', 'status', 'deadline', 'start_at', 'updated_at', 'task', 'users')
        read_only_fields = ('id', 'updated_at', 'task', 'status')

class MiniTaskStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiniTask
        fields = ('id', 'status')

class TaskSerializer(serializers.ModelSerializer):
    manager = UserGeneralSerializer(read_only=True)
    users = UserGeneralSerializer(many=True)
    class Meta:
        model = Task
        fields = ('id', 'title', 'content', 'status', 'deadline', 'start_at', 'updated_at', 'manager', 'users')
        read_only_fields = ('id', 'updated_at')

class TaskGeneralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'content', 'status', 'deadline', 'start_at', 'updated_at', 'manager', 'users')
        read_only_fields = ('id', 'updated_at')