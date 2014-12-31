# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pin.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True, verbose_name='Last update date', auto_now=True)),
                ('source_domain', models.CharField(verbose_name='Domain pin comes from', max_length=254, null=True, blank=True)),
                ('source', models.URLField(verbose_name='Web page pin comes from', max_length=2000, null=True, blank=True)),
                ('description', models.TextField(verbose_name='Pin description')),
                ('policy', models.PositiveIntegerField(null=True, blank=True)),
                ('owner_rate', models.PositiveSmallIntegerField(default=0, verbose_name='Rate')),
                ('added_via', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('sha1', models.CharField(unique=True, max_length=42, db_index=True)),
                ('source_file', models.ImageField(upload_to=pin.models.set_pathname, storage=pin.models.ResourceFileSystemStorage())),
                ('source_file_url', models.URLField(verbose_name='Source of original picture', max_length=2000, null=True, blank=True)),
                ('n_pins', models.PositiveIntegerField(default=0, verbose_name='Board number')),
                ('width', models.PositiveIntegerField(default=0, verbose_name='Pin width, in pixels')),
                ('height', models.PositiveIntegerField(default=0, verbose_name='Pin height, in pixels')),
                ('size', models.PositiveIntegerField(default=0, verbose_name='Size of picture, in bytes')),
                ('type', models.CharField(verbose_name='Type of file', max_length=30)),
                ('previews_path', models.CharField(max_length=254, null=True, blank=True)),
                ('user', models.ForeignKey(verbose_name='User who originaly uploaded or downloaded resource.', to=settings.AUTH_USER_MODEL, null=True, blank=True)),
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
