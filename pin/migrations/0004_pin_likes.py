# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('pin', '0003_auto_20150213_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='likes',
            field=models.ManyToManyField(null=True, blank=True, related_name='likes', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
