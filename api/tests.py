from apps.orders.models import Order, ProductOrder
from apps.products.models import Product
from apps.tables.models import Table
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TableMapTests(APITestCase):
    maxDiff = None  # to see the full details in case of failure


    def test_login(self):
        user = User.objects.create(username="foo")
        user.set_password("bar")
        user.save()

        response = self.client.post(reverse("login"), {"username": "foo", "password": "bar"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"role": "ninguno"})

        user.is_superuser = True
        user.save()

        response = self.client.post(reverse("login"), {"username": "foo", "password": "bar"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"role": "encargado"})


    def test_stats(self):
        table_1 = Table.objects.create(x=1, y=1, name="foo")
        table_2 = Table.objects.create(x=2, y=2, name="bar")

        product_1 = Product.objects.create(name="Foo", price=11.11, image="https://foo.com/bar.png")
        product_2 = Product.objects.create(name="Bar", price=22.22, image="https://foo.com/bar.png")
        product_3 = Product.objects.create(name="Baz", price=33.33, image="https://foo.com/bar.png")

        order_1 = Order.objects.create(table=table_1)
        order_2 = Order.objects.create(table=table_2)

        product_order_1 = ProductOrder.objects.create(quantity=10, product=Product.objects.get(id=1), order=Order.objects.get(id=1))
        product_order_2 = ProductOrder.objects.create(quantity=2, product=Product.objects.get(id=2), order=Order.objects.get(id=2))
        product_order_3 = ProductOrder.objects.create(quantity=3, product=Product.objects.get(id=3), order=Order.objects.get(id=1))
        product_order_4 = ProductOrder.objects.create(quantity=10, product=Product.objects.get(id=1), order=Order.objects.get(id=2))

        response = self.client.get(reverse("stats"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "product_more": {
                    "id": product_1.id,
                    "name": product_1.name,
                    "price": str(product_1.price),
                    "image": product_1.image,
                    "purchases": 20  # new field
                },
                "table_more": {
                    "id": table_1.id,
                    "name": table_1.name,
                    "x": table_1.x,
                    "y": table_1.y,
                    "join_with": table_1.join_with,
                    "join_direction": None,
                    "order": table_1.order.id,
                    "money": 211.09  # new field
                },
                "product_less": {
                    "id": product_2.id,
                    "name": product_2.name,
                    "price": str(product_2.price),
                    "image": product_2.image,
                    "purchases": 2  # new field
                },
                "table_less": {
                    "id": table_2.id,
                    "name": table_2.name,
                    "x": table_2.x,
                    "y": table_2.y,
                    "join_with": table_2.join_with,
                    "join_direction": None,
                    "order": table_2.order.id,
                    "money": 155.54  # new field
                }
            }
        )


    def test_basic_flow(self):
        tables_url = reverse("tables-list")
        products_url = reverse("products-list")
        orders_url = reverse("orders-list")

        # create tables
        data = {
            "x": 1,
            "y": 1,
            "name": "Mesa 1"
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
                    "name": "Mesa 1",
                    "x": 1,
                    "y": 1,
                    "order": None,
                    "join_with": None,
                    "join_direction": None,
                },
                {
                    "id": 2,
                    "name": "Nueva mesa",
                    "x": 2,
                    "y": 2,
                    "order": None,
                    "join_with": None,
                    "join_direction": None,
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

        # open table (creating a new order)
        data = {
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
                "name": "Mesa 1",
                "x": 1,
                "y": 1,
                "order": 1,
                "join_with": None,
                "join_direction": None,
            }
        )

        # create new product order
        data = {
            "product": 1,
            "quantity": 5,
        }
        response = self.client.post(reverse("orders-append", args=[Order.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductOrder.objects.count(), 1)

        # create a second product order
        data = {
            "product": 2,
            "quantity": 3,
        }
        response = self.client.post(reverse("orders-append", args=[Order.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductOrder.objects.count(), 2)

        # update the first product
        data = {
            "product": 1,
            "quantity": 4,
        }
        response = self.client.post(reverse("orders-append", args=[Order.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProductOrder.objects.count(), 2)

        # get the total amount at the moment
        response = self.client.get(reverse("orders-detail", args=[Order.objects.first().id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_1 = Product.objects.first()
        product_2 = Product.objects.last()
        self.assertDictEqual(
            response.json(),
            {
                "id": 1,
                "table": 1,
                "order": [
                    {"product": 1, "quantity": 4},
                    {"product": 2, "quantity": 3}
                ],
                "total": float(
                    product_1.price * ProductOrder.objects.get(product=product_1).quantity
                    + product_2.price * ProductOrder.objects.get(product=product_2).quantity
                )
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
                "name": "Mesa 1",
                "x": 1,
                "y": 1,
                "order": 1,
                "join_with": 2,
                "join_direction": None,
            }
        )

        # get the other table merged
        response = self.client.get(reverse("tables-detail", args=[Table.objects.last().id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": 2,
                "name": "Nueva mesa",
                "x": 2,
                "y": 2,
                "order": None,
                "join_with": None,  # the 1to1 exist on the table moved,
                "join_direction": None,
            }
        )

        # unmerge the table
        data = {
            "join_with": None
        }
        response = self.client.patch(reverse("tables-detail", args=[Table.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get table
        response = self.client.get(reverse("tables-detail", args=[Table.objects.first().id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json(),
            {
                "id": 1,
                "name": "Mesa 1",
                "x": 1,
                "y": 1,
                "order": 1,
                "join_with": None,
                "join_direction": None,
            }
        )

        # close table (remove relationship)
        data = {
            "table": None
        }
        response = self.client.patch(reverse("orders-detail", args=[Order.objects.first().id]), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the table
        response = self.client.get(tables_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictEqual(
            response.json()[0],
            {
                "id": 1,
                "name": "Mesa 1",
                "x": 1,
                "y": 1,
                "order": None,
                "join_with": None,
                "join_direction": None,
            }
        )
