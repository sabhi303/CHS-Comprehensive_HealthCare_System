# Generated by Django 2.2 on 2021-01-29 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0003_auto_20210129_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='rdate',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 29, 16, 10, 26, 643661)),
        ),
    ]
