# Generated by Django 5.0.6 on 2024-07-04 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0016_rename_price_order_items_total_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
