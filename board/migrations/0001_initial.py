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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Creation date')),
                ('date_updated', models.DateTimeField(auto_now_add=True, auto_now=True, verbose_name='Last update date')),
                ('title', models.CharField(max_length=254, verbose_name='Title')),
                ('slug', models.SlugField(max_length=254, verbose_name='Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Board description')),
                ('pin_default_description', models.TextField(help_text='Pin default description used if pinned image has no alt attribute.', blank=True, null=True, verbose_name='Default description')),
                ('n_pins', models.PositiveIntegerField(default=0, verbose_name='Pins number')),
                ('policy', models.PositiveIntegerField(default=1, choices=[(0, 'Private'), (1, 'Public')], verbose_name='Policy')),
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
