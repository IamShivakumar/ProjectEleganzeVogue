# Generated by Django 5.0.6 on 2024-06-14 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0005_size_products_productimages_product_sku'),
    ]

    operations = [
        migrations.RenameField(
            model_name='size',
            old_name='model_code',
            new_name='size_code',
        ),
        migrations.RenameField(
            model_name='size',
            old_name='model_description',
            new_name='size_description',
        ),
    ]
