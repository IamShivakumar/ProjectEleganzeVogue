# Generated by Django 5.0.6 on 2024-07-03 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_useraddress_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='phone',
            field=models.PositiveBigIntegerField(null=True),
        ),
    ]
