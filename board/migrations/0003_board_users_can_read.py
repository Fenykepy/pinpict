# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0002_auto_20141231_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='users_can_read',
            field=models.ManyToManyField(related_name='users_can_read', blank=True, null=True, verbose_name='Users who can read if private', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
