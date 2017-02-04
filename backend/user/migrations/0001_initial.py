# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', verbose_name='username', max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(blank=True, verbose_name='first name', max_length=30)),
                ('last_name', models.CharField(blank=True, verbose_name='last name', max_length=30)),
                ('email', models.EmailField(blank=True, verbose_name='email address', max_length=75)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('slug', models.SlugField(verbose_name='Slug', unique=True, max_length=30)),
                ('uuid', models.CharField(blank=True, null=True, max_length=42)),
                ('uuid_expiration', models.DateTimeField(blank=True, null=True)),
                ('avatar', models.ImageField(blank=True, null=True, help_text='A picture to download as avatar.', verbose_name='Avatar', upload_to='images/avatars')),
                ('website', models.URLField(blank=True, null=True, help_text='A link to your website.', verbose_name='Site web', max_length=2000)),
                ('facebook_link', models.URLField(blank=True, null=True, help_text='A link to your facebook page.', verbose_name='Facebook', max_length=2000)),
                ('flickr_link', models.URLField(blank=True, null=True, help_text='A link to your flickr page.', verbose_name='Flickr', max_length=2000)),
                ('twitter_link', models.URLField(blank=True, null=True, help_text='A link to your twitter page.', verbose_name='Twitter', max_length=2000)),
                ('gplus_link', models.URLField(blank=True, null=True, help_text='A link to your google + page.', verbose_name='Google +', max_length=2000)),
                ('pinterest_link', models.URLField(blank=True, null=True, help_text='A link to your pinterest page.', verbose_name='Pinterest', max_length=2000)),
                ('vk_link', models.URLField(blank=True, null=True, help_text='A link to your vkontakte page.', verbose_name='Vkontakte', max_length=2000)),
                ('n_public_pins', models.PositiveIntegerField(default=0, verbose_name="Public pins'number")),
                ('n_pins', models.PositiveIntegerField(default=0, verbose_name="Pins'number")),
                ('n_boards', models.PositiveIntegerField(default=0, verbose_name="Boards'number")),
                ('n_public_boards', models.PositiveIntegerField(default=0, verbose_name="Public Boards'number")),
                ('groups', models.ManyToManyField(related_name='user_set', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', blank=True, related_query_name='user', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_name='user_set', to='auth.Permission', help_text='Specific permissions for this user.', blank=True, related_query_name='user', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
    ]
