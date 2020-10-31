from django.db import models


class Order(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    table = models.ForeignKey("tables.Table", on_delete=models.CASCADE)
