from apps.products.models import Product
from apps.tables.models import Table
from rest_framework import mixins, routers, serializers, viewsets

from .serializers import ProductSerializer, TableSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ["id", "name",  "price"]


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    filter_fields = ["id", "x", "y", "current_order", "join_with"]
