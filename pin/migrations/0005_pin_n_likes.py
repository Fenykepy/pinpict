# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0004_pin_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='n_likes',
            field=models.PositiveIntegerField(default=0, verbose_name='Number of likes'),
            preserve_default=True,
        ),
    ]
