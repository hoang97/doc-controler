# Generated by Django 3.2.5 on 2021-09-06 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsmt', '0006_alter_attacklog_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attacklog',
            name='timestamp',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date_created',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='xfile',
            name='date_created',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='xfilechange',
            name='date_created',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
