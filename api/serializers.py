from apps.orders.models import Order, ProductOrder
from apps.products.models import Product
from apps.tables.models import Table
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "image",
            "price"
        )


class TableSerializer(serializers.ModelSerializer):
    orders = serializers.SerializerMethodField()

    def get_orders(self, obj):
        return obj.order_set.all().values_list("id", flat=True).order_by("-id")

    class Meta:
        model = Table
        fields = (
            "id",
            "name",
            "x",
            "y",
            "join_with",
            "orders"
        )


class OrderSerializer(serializers.ModelSerializer):
    product_orders = serializers.SerializerMethodField()

    def get_product_orders(self, obj):
        return ProductOrder.objects.filter(order=obj).values("product", "quantity")

    class Meta:
        model = Order
        fields = (
            "id",
            "table",
            "product_orders",
            "total"
        )


class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = (
            "id",
            "quantity",
            "product",
            "order",
        )
