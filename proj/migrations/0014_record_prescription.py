# Generated by Django 2.2 on 2021-05-13 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proj', '0013_messages_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='prescription',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
