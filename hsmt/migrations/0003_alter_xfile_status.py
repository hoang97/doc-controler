# Generated by Django 3.2.5 on 2021-07-21 17:55

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('hsmt', '0002_auto_20210719_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xfile',
            name='status',
            field=django_fsm.FSMField(choices=[('IN', 'khởi tạo'), ('ED', 'đang sửa đổi'), ('CH', 'đang kiểm định'), ('AP', 'đang phê duyệt'), ('DO', 'đã hoàn thiện')], default='IN', max_length=2),
        ),
    ]
