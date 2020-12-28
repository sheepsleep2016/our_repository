# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2019-05-27 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20190527_0843'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_sum',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, verbose_name='订单金额'),
        ),
    ]
