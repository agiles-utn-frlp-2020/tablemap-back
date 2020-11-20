from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum


class Order(models.Model):
    table = models.OneToOneField("tables.Table", on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(
        "products.Product",
        through="ProductOrder",
    )

    @property
    def total(self):
        lines = ProductOrder.objects.filter(
            order=self
        ).annotate(
            subtotal=ExpressionWrapper(
                F("quantity") * F("product__price"),
                output_field=DecimalField()
            )
        )
        total = lines.aggregate(total=Sum("subtotal")).get("total")

        return total


class ProductOrder(models.Model):
    quantity = models.IntegerField(null=True)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
