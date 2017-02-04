# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_auto_20150213_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='root_uri',
            field=models.URLField(blank=True, null=True, verbose_name='Home page URI, without trailing slash'),
            preserve_default=True,
        ),
    ]
