# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_updated', models.DateTimeField(verbose_name='Last update date', auto_now=True, auto_now_add=True)),
                ('title', models.CharField(verbose_name='Title', max_length=254)),
                ('slug', models.SlugField(verbose_name='Slug', max_length=254)),
                ('description', models.TextField(verbose_name='Board description', null=True, blank=True)),
                ('pin_default_description', models.TextField(verbose_name='Default description', null=True, blank=True, help_text='Pin default description used if pinned image has no alt attribute.')),
                ('n_pins', models.PositiveIntegerField(verbose_name='Pins number', default=0)),
                ('policy', models.PositiveIntegerField(verbose_name='Policy', default=1, choices=[(0, 'Private'), (1, 'Public')])),
                ('order', models.PositiveIntegerField(default=100000)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order', 'date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='board',
            unique_together=set([('user', 'slug')]),
        ),
    ]
