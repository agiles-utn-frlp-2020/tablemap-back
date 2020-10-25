from apps.products.models import Product
from rest_framework import mixins, viewsets

from apps.tables.models import Table
from .serializers import ProductSerializer, TableSerializer

from rest_framework import routers, serializers
#from rest_framework import generics


class ProductViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_fields = ["id", "name",  "price"]


class TableViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    #filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    filter_fields = ["id", "position_x",
                     "position_y", "currentorder", "joinWith"]
