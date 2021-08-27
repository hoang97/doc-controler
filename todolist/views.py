from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from todolist.models import Task, MiniTask
from django.shortcuts import get_object_or_404, redirect, render


# API here
def JsonResponseError(msg):
    return JsonResponse({"status": -1, "msg": msg})


def JsonResponseSuccess(data):
    return JsonResponse({"status": 0, "data": data})


@login_required
def add_task(request):
    msg = ''
    if request.user.info.position.id == 0:
        msg = "Không đủ quyền tạo công việc"
        return JsonResponseError(msg)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        start_at = datetime.strptime(request.POST.get('start_at', ''), '%Y-%m-%d')
        deadline = datetime.strptime(request.POST.get('deadline', ''), '%Y-%m-%d')
        if deadline < start_at:
            msg = "Hạn thực hiện phải sau ngày bắt đầu"
            return JsonResponseError(msg)

        manager = request.user

        usernames = request.POST.get('users', '').split(',')
        users = []
        for username in usernames:
            if User.objects.filter(username=username).exists():
                users.append(User.objects.get(username=username))
            else:
                msg = "Người dùng được thêm không có trong danh sách người thực hiện"
                return JsonResponseError(msg)

        if not (title and content and start_at and deadline):
            msg = "Hãy điền đầy đủ thông tin"
        else:
            task = Task.objects.create(title=title, content=content, start_at=start_at,
                                       deadline=deadline, manager=manager)
            task.save()
            task.users.set(users)
            task.save()
            return JsonResponseSuccess('Tạo công việc thành công!')

    return JsonResponseError(msg)


@login_required
def add_mini_task(request, task_id):
    msg = ''
    if not Task.objects.filter(id=task_id).exists():
        msg = "Công việc không tồn tại"
        return JsonResponseError(msg)

    task = Task.objects.get(id=task_id)

    if request.user.username != task.manager.username:
        msg = "Chỉ có người quản lý mới có quyền thêm nhiệm vụ"
        return JsonResponseError(msg)

    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        start_at = datetime.strptime(request.POST.get('start_at', ''), '%Y-%m-%d')
        deadline = datetime.strptime(request.POST.get('deadline', ''), '%Y-%m-%d')
        if deadline < start_at:
            msg = "Hạn thực hiện phải sau ngày bắt đầu"
            return JsonResponseError(msg)

        usernames = request.POST.get('users', '').split(',')
        users = []
        for username in usernames:
            if (task.manager.username == username):
                users.append(task.manager)
            elif task.users.filter(username=username).exists():
                users.append(task.users.get(username=username))
            else:
                msg = "Người dùng được thêm không có trong danh sách người thực hiện"
                return JsonResponseError(msg)

        if not (title and content and start_at and deadline):
            msg = "Hãy điền đầy đủ thông tin"
        else:
            mini_task = MiniTask.objects.create(title=title, content=content, start_at=start_at, deadline=deadline,
                                                task=task)
            mini_task.save()
            mini_task.users.set(users)
            mini_task.save()
            return JsonResponseSuccess('Tạo nhiệm vụ thành công!')

    return JsonResponseError(msg)


@login_required
def delete_task(request):
    msg = ''

    task_id = request.POST.get('task_id', '')

    if not Task.objects.filter(id=task_id).exists():
        msg = "Công việc không tồn tại"
        return JsonResponseError(msg)

    task_to_delete = Task.objects.get(id=task_id)

    if request.user.username != task_to_delete.manager.username:
        msg = "Chỉ có người quản lý mới được quyền xóa công việc"
        return JsonResponseError(msg)

    if request.method == 'POST':
        task_to_delete.delete()
        return JsonResponseSuccess('Xóa công việc thành công!')

    return JsonResponseError(msg)


@login_required
def delete_mini_task(request):
    msg = ''

    mini_task_id = request.POST.get('mini_task_id', '')

    if not MiniTask.objects.filter(id=mini_task_id).exists():
        msg = "Công việc không tồn tại"
        return JsonResponseError(msg)

    mini_task_to_delete = MiniTask.objects.get(id=mini_task_id)

    if not mini_task_to_delete:
        msg = "Nhiệm vụ không tồn tại"
        return JsonResponseError(msg)

    if request.user.username != mini_task_to_delete.task.manager.username:
        msg = "Chỉ có người quản lý mới được quyền xóa công việc"
        return JsonResponseError(msg)

    if request.method == 'POST':
        mini_task_to_delete.delete()
        return JsonResponseSuccess('Xóa nhiệm vụ thành công!')

    return JsonResponseError(msg)


@login_required
def get_tasks(request):
    data = {
        'tasks': []
    }

    queryset = Task.objects.all()
    for task in queryset:
        data['tasks'].append({
            'id': task.id,
            'title': task.title,
            'content': task.content,
            'manager': task.manager.username,
            'users': [user.username for user in task.users.all()],
            'status': task.status,
            'deadline': task.deadline,
            'start_at': task.start_at
        })
    return JsonResponseSuccess(data)


@login_required
def get_mini_tasks(request, task_id):
    data = {
        'mini-tasks': []
    }

    task = get_object_or_404(Task, id=task_id)
    if not any([user.username == request.user.username for user in task.users.all()]) and request.user.username != task.manager.username:
        msg = 'Không có quyền truy cập công việc'
        return JsonResponseError(msg)

    for mini_task in task.mini_tasks.all():
        data['mini-tasks'].append({
            'id': mini_task.id,
            'title': mini_task.title,
            'content': mini_task.content,
            'users': [user.username for user in mini_task.users.all()],
            'status': mini_task.status,
            'deadline': mini_task.deadline,
            'start_at': mini_task.start_at
        })
    return JsonResponseSuccess(data)


@login_required
def switch_status(request):
    if request.method == "POST":
        task_id = request.POST.get('task_id', '')
        status = request.POST.get('status', '')

        if not (task_id or status):
            return JsonResponseError('Không đủ dữ liệu')

        if not MiniTask.objects.filter(id=task_id).exists():
            return JsonResponseError('Công việc không tồn tại')
        task_for_change = Task.objects.get(id=task_id)

        task_for_change = Task.objects.get(id=task_id)
        if task_for_change.manager.username != request.user.username:
            return JsonResponseError('Không thể đổi trạng thái nhiệm vụ không phải của mình')

        task_for_change.status = request.POST.get('status', status)
        task_for_change.save()

        return JsonResponseSuccess('Đổi trạng thái thành công')

    return JsonResponseError('')


@login_required
def switch_status_mini_task(request):
    if request.method == "POST":
        mini_task_id = request.POST.get('mini_task_id', '')
        status = request.POST.get('status', '')
        if not (mini_task_id or status):
            return JsonResponseError('Không đủ dữ liệu')

        if not MiniTask.objects.filter(id=mini_task_id).exists():
            return JsonResponseError('Nhiệm vụ không tồn tại')
        mini_task_for_change = MiniTask.objects.get(id=mini_task_id)

        if mini_task_for_change.task.manager.username != request.user.username or \
                any([user.username == request.user.username for user in mini_task_for_change.users.all()]):
            return JsonResponseError('Không thể đổi trạng thái nhiệm vụ không phải của mình')

        if mini_task_for_change.task.manager.username != request.user.username and status == 3:
            return JsonResponseError('Chỉ có người quản lý mới được đổi trạng thái Đã hoàn thiện')

        mini_task_for_change.status = request.POST.get('status', status)
        mini_task_for_change.save()

        return JsonResponseSuccess('Đổi trạng thái thành công')

    return JsonResponseError('')


def task_list_view(request):
    title = 'Danh sách công việc'
    context = {
        'breadcrumb': title,
        'h1header': title,
        'user_layout': request.user
    }
    return render(request, 'todolist/task_list.html', context)


def task_view(request, task_id):
    context = {
        'breadcrumb_sub': Task.objects.get(id=task_id).title,
        'h1header': 'Danh sách nhiệm vụ',
        'task_id': Task.objects.get(id=task_id).id,
        'user_layout': request.user
    }
    return render(request, 'todolist/mini_task_list.html', context)
