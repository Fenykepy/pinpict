# Generated by Django 2.2.6 on 2019-10-20 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_auto_20160821_1659'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='cover1',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='cover2',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='cover3',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='cover4',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='cover5',
            field=models.CharField(max_length=42, null=True),
        ),
        migrations.AlterField(
            model_name='board',
            name='pins_order',
            field=models.CharField(choices=[('date_created', 'Date'), ('owner_rate', 'Rating'), ('source_domain', 'Domain pin comes from')], default='date_created', max_length=254, verbose_name='Order pins by'),
        ),
    ]
