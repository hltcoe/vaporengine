# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 17:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visualizer', '0002_auto_20180620_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='situationframelabel',
            name='resolution',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='situationframelabel',
            name='status',
            field=models.TextField(null=True),
        ),
    ]