from .serializers import OrderSerializer, ProductSerializer, TableSerializer

from rest_framework import mixins, routers, serializers, viewsets

from apps.products.models import Product
from apps.tables.models import Table
from apps.orders.models import Order


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ["id", "name",  "price"]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_fields = ["id", "x", "y", "orders", "join_with"]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
