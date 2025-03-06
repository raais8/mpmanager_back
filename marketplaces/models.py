from django.db import models

class Marketplace(models.Model):
    name = models.CharField(
        max_length=30
    )
    logo_url = models.URLField(
        max_length=500,
        blank=True,
    )
    color = models.CharField(
        max_length=7,
        default="#d1d1d1"
    )

    def __str__(self):
        return self.name