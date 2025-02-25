from django.db import models

class Marketplace(models.Model):
    name = models.CharField(
        max_length=30
    )
    logo_url = models.URLField(
        max_length=500,
        blank=True,
    )

    def __str__(self):
        return self.name