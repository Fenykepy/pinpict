# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150209_2244'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='unread_notifications',
            field=models.PositiveIntegerField(default=0, verbose_name='New notifications'),
            preserve_default=True,
        ),
    ]
