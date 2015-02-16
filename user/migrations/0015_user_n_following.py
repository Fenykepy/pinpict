# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_auto_20150216_1748'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='n_following',
            field=models.PositiveIntegerField(default=0, verbose_name='Followed users number'),
            preserve_default=True,
        ),
    ]
