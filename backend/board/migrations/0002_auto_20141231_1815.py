# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='pins_order',
            field=models.CharField(choices=[('date_created', 'Date'), ('owner_rate', 'Rating'), ('source_domain', 'Domain pin comes from')], blank=True, max_length=254, default='date_created', verbose_name='Order pins by', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='board',
            name='reverse_pins_order',
            field=models.BooleanField(default=False, verbose_name='Descending order'),
            preserve_default=True,
        ),
    ]
