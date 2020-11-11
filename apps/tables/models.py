from django.db import models


class Table(models.Model):
    name = models.CharField(max_length=200)
    x = models.IntegerField()
    y = models.IntegerField()
    orders = models.ManyToManyField("products.Product", through="orders.Order")
    join_with = models.OneToOneField(
        "self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Mesa {self.name} con id {self.id} en [{self.x}, {self.y}]"
