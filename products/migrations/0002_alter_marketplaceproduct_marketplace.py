# Generated by Django 5.1.5 on 2025-02-28 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplaces', '0002_marketplace_logo_url'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marketplaceproduct',
            name='marketplace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='marketplace_products', to='marketplaces.marketplace'),
        ),
    ]
