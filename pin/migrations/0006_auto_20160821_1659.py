# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-21 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0005_pin_n_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Last update date'),
        ),
        migrations.AlterField(
            model_name='pin',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]