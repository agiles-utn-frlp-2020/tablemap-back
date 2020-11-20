from apps.orders.models import Order, ProductOrder
from apps.products.models import Product
from apps.tables.models import Table
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
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


class StatsView(views.APIView):
    def get(self, request, format=None):
        product_with_more_purchases = Product.objects.annotate(
            purchases=Sum("productorder__quantity")
        ).order_by("-purchases")[0]
        product = ProductSerializer(product_with_more_purchases).data
        product["purchases"] = product_with_more_purchases.purchases

        table_which_earn_more_money = Table.objects.annotate(
            money=Sum("order__productorder__product__price")
        ).order_by("-money")[0]
        table = TableSerializer(table_which_earn_more_money).data
        table["money"] = table_which_earn_more_money.money

        return Response(
            {
                "product_with_more_purchases": product,
                "table_which_earn_more_money": table
            },
            status=status.HTTP_200_OK
        )

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
