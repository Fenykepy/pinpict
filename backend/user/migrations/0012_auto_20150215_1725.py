# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_user_px500'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='px500',
            new_name='px500_link',
        ),
    ]
