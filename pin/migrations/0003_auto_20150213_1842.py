# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0002_pin_main'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pin',
            name='added_via',
            field=models.ForeignKey(null=True, blank=True, to='pin.Pin', on_delete=models.CASCADE),
        ),
    ]
