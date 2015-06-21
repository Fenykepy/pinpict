# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_auto_20150217_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='instagram_link',
            field=models.URLField(verbose_name='Instagram', max_length=2000, null=True, blank=True, help_text='A link to your instagram page.'),
            preserve_default=True,
        ),
    ]
