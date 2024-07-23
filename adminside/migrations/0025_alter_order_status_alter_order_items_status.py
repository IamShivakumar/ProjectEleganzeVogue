# Generated by Django 5.0.7 on 2024-07-14 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0024_alter_order_items_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Request Return', 'Request Return'), ('Return Approved', 'Return Approved'), ('Returned', 'Returned')], default='Pending', max_length=150),
        ),
        migrations.AlterField(
            model_name='order_items',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Out for Delivery', 'Out for Delivery'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Request Return', 'Request Return'), ('Return Approved', 'Return Approved'), ('Returned', 'Returned')], default='Pending', max_length=150),
        ),
    ]
