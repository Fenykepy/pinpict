# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pin.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_updated', models.DateTimeField(verbose_name='Last update date', auto_now_add=True, auto_now=True)),
                ('source_domain', models.CharField(blank=True, verbose_name='Domain pin comes from', max_length=254, null=True)),
                ('source', models.URLField(blank=True, verbose_name='Web page pin comes from', max_length=2000, null=True)),
                ('description', models.TextField(verbose_name='Pin description')),
                ('policy', models.PositiveIntegerField(blank=True, null=True)),
                ('owner_rate', models.PositiveSmallIntegerField(default=0, verbose_name='Rate')),
                ('added_via', models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL)),
                ('board', models.ForeignKey(to='board.Board')),
                ('pin_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='pin_user')),
            ],
            options={
                'ordering': ['date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('sha1', models.CharField(db_index=True, unique=True, max_length=42)),
                ('source_file', models.ImageField(storage=pin.models.ResourceFileSystemStorage(), upload_to=pin.models.set_pathname)),
                ('source_file_url', models.URLField(blank=True, verbose_name='Source of original picture', max_length=2000, null=True)),
                ('n_pins', models.PositiveIntegerField(default=0, verbose_name='Board number')),
                ('width', models.PositiveIntegerField(default=0, verbose_name='Pin width, in pixels')),
                ('height', models.PositiveIntegerField(default=0, verbose_name='Pin height, in pixels')),
                ('size', models.PositiveIntegerField(default=0, verbose_name='Size of picture, in bytes')),
                ('type', models.CharField(verbose_name='Type of file', max_length=30)),
                ('previews_path', models.CharField(blank=True, max_length=254, null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True, verbose_name='User who originaly uploaded or downloaded resource.')),
            ],
            options={
                'ordering': ['date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='pin',
            name='resource',
            field=models.ForeignKey(to='pin.Resource'),
            preserve_default=True,
        ),
    ]
