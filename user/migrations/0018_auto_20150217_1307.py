# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0017_user_n_public_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_following_liked_pin',
            field=models.BooleanField(verbose_name='Receive a mail when a user I follow liked a pin', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_pin_like',
            field=models.BooleanField(verbose_name='Receive a mail when a user liked one of my pins', default=True),
            preserve_default=True,
        ),
    ]
