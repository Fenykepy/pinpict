# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='main',
            field=models.BooleanField(verbose_name='Use as main preview', default=False),
            preserve_default=True,
        ),
    ]
