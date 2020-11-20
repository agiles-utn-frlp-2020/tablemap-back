from apps.orders.models import Order, ProductOrder
from apps.products.models import Product
from apps.tables.models import Table
from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (mixins, response, routers, serializers, status,
                            views, viewsets)
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import OrderSerializer, ProductSerializer, TableSerializer


class LoginView(views.APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"role": "encargado" if user.is_superuser else "mozo"},
                status=status.HTTP_200_OK
            )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    def post(self, request, format=None):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

    @action(detail=True, methods=['post'])
    def append(self, request, pk=None):
        order = self.get_object()
        product = Product.objects.get(id=request.data.get("product"))
        quantity = request.data.get("quantity")

        if product and quantity:
            obj, created = ProductOrder.objects.get_or_create(
                product=product,
                order=order
            )

            obj.quantity = quantity
            obj.save()

            if created:
                return Response(status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
