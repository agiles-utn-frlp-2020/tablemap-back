from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.tables.models import Table
from apps.products.models import Product


class TableMapTests(APITestCase):
    def test_merge_tables(self):
        tables_url = reverse("tables-list")
        products_url = reverse("products-list")

        # create table
        data = {
            "x": 1,
            "y": 1
        }
        response = self.client.post(tables_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Table.objects.count(), 1)

        # get tables
        response = self.client.get(tables_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json()[0], 
            {
                "id": 1,
                "x": 1,
                "y": 1,
                "order": None,
                "join_with": []
            }
        )

        # create product
        data = {
            "name": "Honey Beer",
            "image": "https://foo.com/bar.png",
            "price": 99.99
        }
        response = self.client.post(products_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)

        # get products
        response = self.client.get(products_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json()[0], 
            {
                "id": 1,
                "name": "Honey Beer",
                "image": "https://foo.com/bar.png",
                "price": "99.99"
            }
        )


