# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='Users who follow user', related_name='followers_rel_+', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='n_followers',
            field=models.PositiveIntegerField(default=0, verbose_name='Followers number'),
            preserve_default=True,
        ),
    ]
