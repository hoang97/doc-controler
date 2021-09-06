# Generated by Django 3.2.5 on 2021-09-03 08:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('hsmt', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='xfilechange',
            name='approver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='changes_approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfilechange',
            name='checker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='changes_checked', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfilechange',
            name='editor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='changes_edited', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfilechange',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='changes', to='hsmt.xfile'),
        ),
        migrations.AddField(
            model_name='xfile',
            name='approvers',
            field=models.ManyToManyField(related_name='xfiles_can_approve', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfile',
            name='checkers',
            field=models.ManyToManyField(related_name='xfiles_can_check', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfile',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='xfiles_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfile',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
        migrations.AddField(
            model_name='xfile',
            name='editors',
            field=models.ManyToManyField(related_name='xfiles_can_edit', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='xfile',
            name='targets',
            field=models.ManyToManyField(to='hsmt.Target'),
        ),
        migrations.AddField(
            model_name='xfile',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hsmt.xfiletype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='attacklog',
            name='file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attack_logs', to='hsmt.xfile'),
        ),
    ]