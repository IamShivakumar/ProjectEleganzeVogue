# Generated by Django 5.0.6 on 2024-06-18 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0011_cart_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.SmallIntegerField(default=1),
        ),
    ]
