# Generated by Django 5.1.5 on 2025-03-25 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplaces', '0004_alter_marketplace_logo_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='marketplace',
            name='country',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Spain'), (1, 'France')], default=0),
        ),
    ]
