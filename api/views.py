from apps.products.models import Product
from rest_framework import mixins, viewsets

from .serializers import ProductSerializer


class ProductViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
