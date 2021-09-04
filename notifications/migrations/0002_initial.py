# Generated by Django 3.2.5 on 2021-09-03 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='recipient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='log',
            name='actor_ct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_actors', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='log',
            name='notify_to',
            field=models.ManyToManyField(through='notifications.Notification', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='log',
            name='target_ct',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_targets', to='contenttypes.contenttype'),
        ),
    ]
