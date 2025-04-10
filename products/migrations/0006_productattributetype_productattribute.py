# Generated by Django 5.1.5 on 2025-04-02 15:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_marketplaceproduct_enabled'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttributeType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=75)),
                ('data_type', models.PositiveSmallIntegerField(choices=[(1, 'Int'), (2, 'Decimal'), (3, 'String'), (4, 'Text'), (5, 'Date'), (6, 'Datetime'), (7, 'Boolean')])),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('name',), name='unique_name')],
            },
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_type', models.PositiveSmallIntegerField(choices=[(1, 'Int'), (2, 'Decimal'), (3, 'String'), (4, 'Text'), (5, 'Date'), (6, 'Datetime'), (7, 'Boolean')])),
                ('data_int', models.IntegerField(null=True)),
                ('data_decimal', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('data_string', models.CharField(blank=True, max_length=300, null=True)),
                ('data_text', models.TextField(blank=True, null=True)),
                ('data_date', models.DateField(null=True)),
                ('data_datetime', models.DateTimeField(null=True)),
                ('data_boolean', models.BooleanField(null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='products.product')),
                ('attribute_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productattributetype')),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('product', 'attribute_type'), name='unique_product_attribute')],
            },
        ),
    ]
