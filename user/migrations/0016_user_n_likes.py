# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_user_n_following'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='n_likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Liked pins number'),
            preserve_default=True,
        ),
    ]
