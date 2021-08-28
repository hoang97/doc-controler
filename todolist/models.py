from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMIntegerField
from django import forms
from datetime import date

class TaskStatus(models.IntegerChoices):
    """
    Những trạng thái của Task
    """
    INIT = 0, _('khởi tạo')
    EDITING = 1, _('đang thực hiện')
    CHECKING = 2, _('đang kiểm định')
    DONE = 3, _('đã hoàn thiện')


class CommonTask(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=500)
    status = FSMIntegerField(
        choices=TaskStatus.choices,
        default=TaskStatus.INIT,
    )
    deadline = models.DateField(default=date.today)
    start_at = models.DateField(default=date.today)

    # default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title + ' - ' + self.content

    class Meta:
        abstract = True


class Task(CommonTask):
    manager = models.ForeignKey(User, related_name='manage_tasks', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='tasks')


class MiniTask(CommonTask):
    task = models.ForeignKey(Task, related_name='mini_tasks', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='mini_tasks')
