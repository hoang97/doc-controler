# Generated by Django 3.2.5 on 2021-09-05 03:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hsmt', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attacklog',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
