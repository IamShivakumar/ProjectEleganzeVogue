# Generated by Django 5.0.7 on 2024-07-14 12:04

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_useraddress_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_wallet', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_wallet',
            },
        ),
    ]
