# Generated by Django 5.0.6 on 2024-07-04 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_useraddress_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraddress',
            name='country',
        ),
    ]