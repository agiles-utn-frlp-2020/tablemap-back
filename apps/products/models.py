from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.URLField(max_length=755)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.name} cuesta ${self.price}"
