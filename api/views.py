from apps.products.models import Product
from rest_framework import mixins, viewsets

from apps.tables.models import Table
from .serializers import ProductSerializer, TableSerializer


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
