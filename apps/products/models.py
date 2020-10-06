from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="images", max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
