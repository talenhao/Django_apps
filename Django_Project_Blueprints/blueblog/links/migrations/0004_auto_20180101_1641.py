# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-01 16:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('links', '0003_auto_20171228_0608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='in_reply_to',
        ),
        migrations.AddField(
            model_name='comment',
            name='in_reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='links.Comment'),
        ),
    ]
