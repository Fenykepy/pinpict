# Generated by Django 2.2.6 on 2019-11-10 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0013_auto_20191023_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='private',
            field=models.BooleanField(default=False, verbose_name='Private board'),
        ),
    ]