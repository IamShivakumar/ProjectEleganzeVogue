# Generated by Django 5.0.7 on 2024-07-17 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_customuser_wallet_balance_delete_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='street',
            field=models.CharField(max_length=50),
        ),
    ]
