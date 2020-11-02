from django.db import models


class Table(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    orders = models.ManyToManyField("products.Product", through="orders.Order")
    join_with = models.ManyToManyField("self", blank=True)

    def __str__(self):
        return f"Mesa {self.id} en [{self.x}, {self.y}]"
