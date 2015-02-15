# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_user_unread_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='unread_notifications',
            new_name='n_unread_notifications',
        ),
    ]
