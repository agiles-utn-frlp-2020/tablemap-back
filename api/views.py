from apps.orders.models import Order
from apps.products.models import Product
from apps.tables.models import Table
from django.contrib.auth import authenticate, login
from rest_framework import (mixins, response, routers, serializers, status,
                            views, viewsets)

from .serializers import OrderSerializer, ProductSerializer, TableSerializer


class LoginView(views.APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return response.Response(status=status.HTTP_200_OK)
        else:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)

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
