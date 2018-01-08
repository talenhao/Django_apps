# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-08 07:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carrental', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_phone', models.TextField()),
                ('customer_email', models.EmailField(max_length=254)),
                ('booking_start', models.DateField()),
                ('booking_end', models.DateField()),
                ('booking_message', models.TextField()),
                ('is_approved', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='car',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carrental.Car'),
        ),
    ]
