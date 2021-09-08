from copy import deepcopy
from datetime import datetime
from rest_framework import generics, status
from rest_framework.response import Response
from todolist.serializers import *
from todolist.permissions import *
from todolist.models import TaskStatus

def check_time_conflict(start, end):
    start_at = datetime.strptime(start, '%Y-%m-%d').date()
    deadline = datetime.strptime(end, '%Y-%m-%d').date()
    return deadline < start_at

def check_users_conflict(minitask_users, task_users):
    for user in minitask_users:
        if user not in task_users:
            return True
    return False

class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.tasks.all()

class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskGeneralSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Mặc định task được tạo có trạng thái INIT, manager là người tạo
        data = deepcopy(request.data)
        data['status'] = 0
        data['manager'] = request.user.id
        # manager phải có trong users
        if request.user.id not in data['users']:
            data['users'].append(request.user.id)

        if check_time_conflict(data.get('start_at', ''), data.get('deadline', '')):
            return Response("Hạn thực hiện phải sau ngày bắt đầu", status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status.HTTP_201_CREATED, headers=headers)

class TaskRetrieveView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanView]

    def get_queryset(self):
        return self.request.user.tasks.all()

class TaskUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskGeneralSerializer
    permission_classes = [IsAuthenticated, IsTaskManager, CanView]

    def get_queryset(self):
        return self.request.user.tasks.all()

    def update(self, request, *args, **kwargs):
        if check_time_conflict(request.data.get('start_at', ''), request.data.get('deadline', '')):
            return Response("Hạn thực hiện phải sau ngày bắt đầu", status.HTTP_400_BAD_REQUEST)

        task_to_edit = self.get_object()
        if request.data.get('manager') and request.data['manager'] not in list(task_to_edit.users.values_list('id', flat=True)):
            return Response("Quản lí phải có trong danh sách người thực hiện", status.HTTP_400_BAD_REQUEST)
        for mini_task in task_to_edit.mini_tasks.all():
            if check_users_conflict(list(mini_task.users.all()), list(task_to_edit.users.all())):
                msg = "Không thể xóa người vẫn còn đang thực hiện nhiệm vụ"
                return Response(msg, status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

class MiniTaskListView(generics.ListAPIView):
    serializer_class = MiniTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs['pk'])
        return task.mini_tasks.filter(users__id__exact=self.request.user.id)

class MiniTaskCreateView(generics.CreateAPIView):
    serializer_class = MiniTaskGeneralSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Minitask được tạo chỉ cho phép users trong Task tham gia
        task = Task.objects.get(id=self.kwargs['pk'])
        task_users = list(task.users.all().values_list('id', flat=True))
        data = request.data

        if request.user != task.manager:
            return Response('', status.HTTP_403_FORBIDDEN)

        if check_users_conflict(data['users'], task_users):
            return Response('Người thực hiện được thêm không có trong danh sách người thực hiện của Task', status.HTTP_400_BAD_REQUEST)

        if check_time_conflict(data.get('start_at', ''), data.get('deadline', '')):
            return Response("Hạn thực hiện phải sau ngày bắt đầu", status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class MiniTaskRetrieveView(generics.RetrieveAPIView):
    serializer_class = MiniTaskSerializer
    permission_classes = [IsAuthenticated, CanView]
    lookup_url_kwarg = 'minitask_id'

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs['pk'])
        return task.mini_tasks.filter(users__id__exact=self.request.user.id)

class MiniTaskUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MiniTaskGeneralSerializer
    permission_classes = [IsAuthenticated, IsTaskManager]
    lookup_url_kwarg = 'minitask_id'

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs['pk'])
        return task.mini_tasks.filter(users__id__exact=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # Minitask được tạo chỉ cho phép users trong Task tham gia
        task = Task.objects.get(id=self.kwargs['pk'])
        task_users = list(task.users.all().values_list('id', flat=True))
        data = request.data

        if check_users_conflict(data['users'], task_users):
            return Response('Người thực hiện được thêm không có trong danh sách người thực hiện của Task', status.HTTP_400_BAD_REQUEST)

        if check_time_conflict(data.get('start_at', ''), data.get('deadline', '')):
            return Response("Hạn thực hiện phải sau ngày bắt đầu", status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

class MiniTaskSwitchStatus(generics.UpdateAPIView):
    serializer_class = MiniTaskStatusSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'minitask_id'

    def get_queryset(self):
        task = Task.objects.get(id=self.kwargs['pk'])
        return task.mini_tasks.filter(users__id__exact=self.request.user.id)

    def update(self, request, *args, **kwargs):
        # Chỉ user và manager được sửa status, chỉ manager được đổi status Đã hoàn thiện
        minitask = self.get_object()
        status = request.data.get('status')
        if status == TaskStatus.DONE and request.user.id != minitask.task.manager.id:
            return Response("Chỉ có người quản lý mới được đổi trạng thái Đã hoàn thiện", status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
