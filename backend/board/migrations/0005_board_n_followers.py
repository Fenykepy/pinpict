# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0004_auto_20150209_0734'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='n_followers',
            field=models.PositiveIntegerField(verbose_name='Followers number', default=0),
            preserve_default=True,
        ),
    ]
