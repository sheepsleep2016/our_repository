# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-05-23 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_auto_20190521_1055'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='com_isSold',
            field=models.BooleanField(default=False, verbose_name='是否卖出'),
        ),
    ]