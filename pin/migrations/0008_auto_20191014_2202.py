# Generated by Django 2.2.6 on 2019-10-14 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0007_auto_20191014_2112'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pin',
            old_name='pin_user',
            new_name='user',
        ),
    ]