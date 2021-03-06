# Generated by Django 2.2.12 on 2021-05-19 11:37

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AddtionalDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.EmailField(max_length=254)),
                ('name', models.CharField(default='', max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('bdate', models.DateField(null=True)),
                ('address', models.TextField(max_length=50)),
                ('city', models.CharField(max_length=10)),
                ('pin', models.CharField(max_length=6)),
                ('gender', models.CharField(max_length=10)),
                ('profession', models.CharField(default='user', max_length=10)),
                ('notifications', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('profile', models.CharField(default='newassets/images/avatar-1.png', max_length=100)),
                ('designation', models.CharField(max_length=6, null=True)),
                ('rating', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=1), blank=True, null=True, size=None)),
                ('bio', models.CharField(max_length=50, null=True)),
            ],
        ),
    ]
