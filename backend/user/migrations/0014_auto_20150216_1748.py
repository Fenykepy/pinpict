# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_auto_20150216_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(null=True, blank=True, verbose_name='Users who follow user', to=settings.AUTH_USER_MODEL, related_name='following'),
        ),
    ]
