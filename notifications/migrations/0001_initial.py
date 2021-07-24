# Generated by Django 3.2.5 on 2021-07-24 07:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('actor_id', models.PositiveIntegerField()),
                ('target_id', models.PositiveIntegerField()),
                ('verb', models.TextField()),
                ('actor_ct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_actors', to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seen', models.BooleanField(default=False)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='notifications.log')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
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
