# Generated by Django 5.0.7 on 2024-07-31 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminside', '0031_banners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]