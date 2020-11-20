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
    order = serializers.IntegerField(source="order.id", read_only=True)
    class Meta:
        model = Table
        fields = (
            "id",
            "name",
            "x",
            "y",
            "join_with",
            "order",
        )


class OrderSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()

    def get_order(self, obj):
        return ProductOrder.objects.filter(order=obj).values("product", "quantity")

    class Meta:
        model = Order
        fields = (
            "id",
            "table",
            "order",
            "total"
        )
