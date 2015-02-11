# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='receiver',
            field=models.ForeignKey(related_name='receiver', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender',
            field=models.ForeignKey(related_name='sender', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Creation date'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='read',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
