from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.tables.models import Table
from apps.products.models import Product
from apps.orders.models import Order


class TableMapTests(APITestCase):
    def test_basic_flow(self):
        tables_url = reverse("tables-list")
        products_url = reverse("products-list")
        orders_url = reverse("orders-list")

        # create tables
        data = {
            "x": 1,
            "y": 1
        }
        response = self.client.post(tables_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)

        data = {
            "x": 2,
            "y": 2
        }
        response = self.client.post(tables_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 2)

        # get tables
        response = self.client.get(tables_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(), 
            [
                {
                    "id": 1,
                    "x": 1,
                    "y": 1,
                    "orders": [],
                    "join_with": None
                },
                {
                    "id": 2,
                    "x": 2,
                    "y": 2,
                    "orders": [],
                    "join_with": None
                }
            ]
        )

        # create products
        product_1 = {
            "name": "Birra",
            "image": "https://foo.com/bar.png",
            "price": 99.99
        }
        response = self.client.post(products_url, product_1, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        product_2 = {
            "name": "Papas",
            "image": "https://bar.com/baz.png",
            "price": 120
        }
        response = self.client.post(products_url, product_2, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

        # get products
        response = self.client.get(products_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": 1,
                    "name": "Birra",
                    "image": "https://foo.com/bar.png",
                    "price": "99.99"
                },
                {
                    "id": 2,
                    "name": "Papas",
                    "image": "https://bar.com/baz.png",
                    "price": "120.00"
                }
            ]
        )

        # create new order
        data = {
            "quantity": 5,
            "product": 1,  # Birra
            "table": 1
        }
        response = self.client.post(orders_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)

        # get table 1
        response = self.client.get(reverse("tables-detail", args=[Table.objects.first().id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(), 
            {
                "id": 1,
                "x": 1,
                "y": 1,
                "orders": [1],
                "join_with": None
            }
        )

        # merge table 1 with table 2
        data = {
            "join_with": Table.objects.last().id
        }
        response = self.client.patch(reverse("tables-detail", args=[Table.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get table
        response = self.client.get(reverse("tables-detail", args=[Table.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(), 
            {
                "id": 1,
                "x": 1,
                "y": 1,
                "orders": [1],
                "join_with": 2
            }
        )

        # get the other table merged
        response = self.client.get(reverse("tables-detail", args=[Table.objects.last().id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": 2,
                "x": 2,
                "y": 2,
                "orders": [],
                "join_with": None  # the 1to1 exist on the table moved
            }
        )