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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('date_created', models.DateTimeField(verbose_name='Creation date', auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Last update date', auto_now_add=True)),
                ('title', models.CharField(max_length=254, verbose_name='Title')),
                ('slug', models.SlugField(max_length=254, verbose_name='Slug')),
                ('description', models.TextField(blank=True, verbose_name='Board description', null=True)),
                ('pin_default_description', models.TextField(help_text='Pin default description used if pinned image has no alt attribute.', blank=True, verbose_name='Default description', null=True)),
                ('n_pins', models.PositiveIntegerField(verbose_name='Pins number', default=0)),
                ('policy', models.PositiveIntegerField(verbose_name='Policy', default=1, choices=[(0, 'Private'), (1, 'Public')])),
                ('order', models.PositiveIntegerField(default=100000)),
                ('pins_order', models.CharField(max_length=254, blank=True, verbose_name='Order pins by', choices=[('date_created', 'Date'), ('owner_rate', 'Rating'), ('source_domain', 'Domain pin comes from')], null=True, default='date_created')),
                ('reverse_pins_order', models.BooleanField(verbose_name='Descending order', default=False)),
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
