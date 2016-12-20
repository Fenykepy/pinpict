# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import pin.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_auto_20141231_1815'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Last update date', auto_now_add=True)),
                ('source_domain', models.CharField(null=True, verbose_name='Domain pin comes from', max_length=254, blank=True)),
                ('source', models.URLField(null=True, verbose_name='Web page pin comes from', max_length=2000, blank=True)),
                ('description', models.TextField(verbose_name='Pin description')),
                ('policy', models.PositiveIntegerField(null=True, blank=True)),
                ('owner_rate', models.PositiveSmallIntegerField(verbose_name='Rate', default=0)),
                ('added_via', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('board', models.ForeignKey(to='board.Board')),
                ('pin_user', models.ForeignKey(related_name='pin_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('sha1', models.CharField(db_index=True, max_length=42, unique=True)),
                ('source_file', models.ImageField(storage=pin.models.ResourceFileSystemStorage(), upload_to=pin.models.set_pathname)),
                ('source_file_url', models.URLField(null=True, verbose_name='Source of original picture', max_length=2000, blank=True)),
                ('n_pins', models.PositiveIntegerField(verbose_name='Board number', default=0)),
                ('width', models.PositiveIntegerField(verbose_name='Pin width, in pixels', default=0)),
                ('height', models.PositiveIntegerField(verbose_name='Pin height, in pixels', default=0)),
                ('size', models.PositiveIntegerField(verbose_name='Size of picture, in bytes', default=0)),
                ('type', models.CharField(verbose_name='Type of file', max_length=30)),
                ('previews_path', models.CharField(null=True, max_length=254, blank=True)),
                ('user', models.ForeignKey(null=True, verbose_name='User who originaly uploaded or downloaded resource.', blank=True, to=settings.AUTH_USER_MODEL)),
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
