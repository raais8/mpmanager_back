from django.db import models

from marketplaces.models import Marketplace

class Product(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=250,
    )
    sku = models.CharField(
        max_length=50,
    )
    reference = models.CharField(
        max_length=50,
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField()

class MarketplaceProduct(models.Model):
    marketplace = models.ForeignKey(
        Marketplace,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )