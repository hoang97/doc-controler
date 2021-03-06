# Generated by Django 3.2.5 on 2021-09-03 08:48

from django.db import migrations, models
import django.utils.timezone
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AttackLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField()),
                ('name', models.TextField(blank=True)),
                ('content', models.TextField(blank=True)),
                ('attacker', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('object_id', models.PositiveIntegerField()),
                ('body', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('type', models.PositiveIntegerField(choices=[(1, 'hướng'), (2, 'nhóm mục tiêu'), (3, 'địa bàn')])),
            ],
        ),
        migrations.CreateModel(
            name='XFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=120)),
                ('description', models.TextField(blank=True)),
                ('status', django_fsm.FSMIntegerField(choices=[(0, 'khởi tạo'), (1, 'đang sửa đổi'), (2, 'đang kiểm định'), (3, 'đang phê duyệt'), (4, 'đã hoàn thiện')], default=0, protected=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('content', models.TextField(blank=True)),
                ('version', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='XFileChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('date_created', models.DateField(default=django.utils.timezone.now)),
                ('date_edited', models.DateField(blank=True, null=True)),
                ('date_submited', models.DateField(blank=True, null=True)),
                ('date_checked', models.DateField(blank=True, null=True)),
                ('date_approved', models.DateField(blank=True, null=True)),
                ('name', models.CharField(max_length=120)),
                ('content', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='XFileType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('example_content', models.TextField()),
            ],
        ),
    ]
