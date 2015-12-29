# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 09:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('created', models.DateTimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='Employee',
        ),
    ]
