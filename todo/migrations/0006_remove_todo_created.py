# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 10:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20151229_1038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='created',
        ),
    ]
