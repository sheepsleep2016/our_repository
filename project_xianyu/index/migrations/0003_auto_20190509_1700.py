# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-05-09 09:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20190509_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity',
            name='com_isactive',
            field=models.BooleanField(default=False, verbose_name='激活'),
        ),
        migrations.AddField(
            model_name='users',
            name='gender',
            field=models.IntegerField(max_length=6, null=True, verbose_name='性别'),
        ),
        migrations.AddField(
            model_name='users',
            name='using_date',
            field=models.DateField(null=True, verbose_name='注册时间'),
        ),
        migrations.AlterField(
            model_name='commodity',
            name='commodity_discrib',
            field=models.TextField(max_length=500, null=True, verbose_name='商品描述'),
        ),
    ]
