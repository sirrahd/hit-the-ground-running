# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-20 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='tenant_id',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
