# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-05-27 08:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0009_auto_20190525_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user_pwd',
            field=models.CharField(max_length=160, verbose_name='密码'),
        ),
    ]