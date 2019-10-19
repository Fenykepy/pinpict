# Generated by Django 2.2.6 on 2019-10-14 19:12

from django.db import migrations, models
import pin.models


class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0006_auto_20160821_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='pin',
            name='sha1',
            field=models.CharField(db_index=True, max_length=42, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='pin',
            name='source_file',
            field=models.ImageField(null=True, storage=pin.models.PinFileSystemStorage(), upload_to=pin.models.set_pathname),
        ),
        migrations.AddField(
            model_name='pin',
            name='source_file_url',
            field=models.URLField(blank=True, max_length=2000, null=True, verbose_name='Source of original picture'),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=254, primary_key=True, serialize=False)),
                ('pins', models.ManyToManyField(blank=True, to='pin.Pin')),
            ],
        ),
    ]