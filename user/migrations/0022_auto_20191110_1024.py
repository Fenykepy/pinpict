# Generated by Django 2.2.6 on 2019-11-10 10:24

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20191014_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, help_text='A picture to download as avatar.', null=True, storage=user.models.AvatarFileSystemStorage(), upload_to=user.models.set_avatar_pathname, verbose_name='Avatar'),
        ),
    ]
