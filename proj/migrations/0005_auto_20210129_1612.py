# Generated by Django 2.2 on 2021-01-29 16:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0004_auto_20210129_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='rdate',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 29, 16, 12, 7, 790762, tzinfo=utc)),
        ),
    ]
