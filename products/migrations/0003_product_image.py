# Generated by Django 5.1.5 on 2025-03-01 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_marketplaceproduct_marketplace'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(null=True),
        ),
    ]
