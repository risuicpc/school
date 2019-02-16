# Generated by Django 2.1.4 on 2019-01-30 17:23

from django.db import migrations
from django.core.management import call_command

def loadfixture(apps, schema_editor):
    call_command('loaddata', 'initial_data.json')

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(loadfixture),
    ]