# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_auto_20150213_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_allow_read',
            field=models.BooleanField(verbose_name="Receive a mail when a user allows me to see one of it's private boards", default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_board_follower',
            field=models.BooleanField(verbose_name='Receive a mail when a user starts to follow one of my boards', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_following_add_board',
            field=models.BooleanField(verbose_name='Receive a mail when following user add a new board', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_following_add_pin',
            field=models.BooleanField(verbose_name='Receive a mail when following user add a new pin', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_reppinned',
            field=models.BooleanField(verbose_name='Receive a mail when one of my pins are pinned', default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='mail_user_follower',
            field=models.BooleanField(verbose_name='Receive a mail when a user starts to follow me', default=True),
            preserve_default=True,
        ),
    ]
