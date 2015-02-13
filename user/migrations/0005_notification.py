# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('user', '0004_auto_20150212_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date', models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='Creation date')),
                ('title', models.TextField(null=True, blank=True, verbose_name='Title')),
                ('read', models.BooleanField(default=False, db_index=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('receiver', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='receiver')),
                ('sender', models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, related_name='sender')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
