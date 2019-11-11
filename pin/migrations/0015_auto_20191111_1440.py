# Generated by Django 2.2.6 on 2019-11-11 14:40

from django.db import migrations


def move_policy_to_private(apps, schema_editor):
     Pin = apps.get_model('pin', 'Pin')
     for pin in Pin.objects.all():
        if pin.policy == 1:
            pin.private = False
        else:
            pin.private = True
        pin.save()



class Migration(migrations.Migration):

    dependencies = [
        ('pin', '0014_pin_private'),
    ]

    operations = [
        migrations.RunPython(move_policy_to_private)
    ]
