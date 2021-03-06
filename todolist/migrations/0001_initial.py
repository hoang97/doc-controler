# Generated by Django 3.2.5 on 2021-09-04 09:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
                ('status', django_fsm.FSMIntegerField(choices=[(0, 'khởi tạo'), (1, 'đang thực hiện'), (2, 'đang kiểm định'), (3, 'đã hoàn thiện')], default=0)),
                ('deadline', models.DateField(default=datetime.date.today)),
                ('start_at', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manage_tasks', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MiniTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=500)),
                ('status', django_fsm.FSMIntegerField(choices=[(0, 'khởi tạo'), (1, 'đang thực hiện'), (2, 'đang kiểm định'), (3, 'đã hoàn thiện')], default=0)),
                ('deadline', models.DateField(default=datetime.date.today)),
                ('start_at', models.DateField(default=datetime.date.today)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mini_tasks', to='todolist.task')),
                ('users', models.ManyToManyField(related_name='mini_tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
