from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from todolist.models import Task, MiniTask

class IsTaskManager(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Task):
            return request.user.id == obj.manager.id
        elif isinstance(obj, MiniTask):
            return request.user.id == obj.task.manager.id
        else:
            raise Exception('Unexpected object type')

class CanView(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in list(obj.users.all())
        