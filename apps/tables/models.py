from django.db import models

from apps.products.models import Product


class Table(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    order = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    join_with = models.ManyToManyField("self", null=True)

    def __str__(self):
        return f"Mesa {self.id} en [{self.x}, {self.y}]"
