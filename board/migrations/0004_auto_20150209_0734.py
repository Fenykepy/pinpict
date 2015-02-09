# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0003_board_users_can_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='followers',
            field=models.ManyToManyField(null=True, related_name='board_followers', blank=True, verbose_name='Users who follow board', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='board',
            name='users_can_read',
            field=models.ManyToManyField(null=True, related_name='users_can_read', blank=True, verbose_name='Users who can see board if private', to=settings.AUTH_USER_MODEL),
        ),
    ]
