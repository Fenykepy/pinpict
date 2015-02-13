# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20150213_2200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='mail_reppinned',
            new_name='mail_repinned',
        ),
    ]
