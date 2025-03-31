from django.db import models

class Country(models.IntegerChoices):
    ES = 0, "Spain"
    FR = 1, "France"

class Marketplace(models.Model):
    name = models.CharField(
        max_length=30
    )
    country = models.PositiveSmallIntegerField(
        choices=Country.choices,
        default=Country.ES,
    )
    logo_url = models.URLField(
        max_length=2048,
        blank=True,
    )
    color = models.CharField(
        max_length=7,
        default="#d1d1d1"
    )

    def __str__(self):
        return self.name