# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_user_root_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='px500',
            field=models.URLField(blank=True, null=True, max_length=2000, help_text='A link to your 500px page.', verbose_name='500px'),
            preserve_default=True,
        ),
    ]
