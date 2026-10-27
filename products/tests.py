from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Product
from .serializers import ProductSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


class ProductSerializerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="owner",
            password="test-password-123"
        )

        cls.other_user = User.objects.create_user(
            username="other",
            password="test-password-456"
        )

        cls.product = Product.objects.create(
            name="Keyboard",
            description="Mechanical keyboard",
            price="100.00",
            sale_price="80.00",
            stock=5,
            owner=cls.owner
        )

    def valid_payload(self):
        return {
            "name": "Mouse",
            "description": "Wireless mouse",
            "price": "100.00",
            "sale_price": "80.00",
            "stock": 10,
            "is_active": True,
        }

    def test_valid_product_data(self):
        serializer = ProductSerializer(
            data=self.valid_payload()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

    def test_negative_price_is_rejected(self):
        data = self.valid_payload()
        data["price"] = "-10.00"

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_sale_price_must_be_lower(self):
        data = self.valid_payload()
        data["sale_price"] = "100.00"

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("sale_price", serializer.errors)

    def test_partial_update_checks_existing_price(self):
        serializer = ProductSerializer(
            instance=self.product,
            data={"sale_price": "120.00"},
            partial=True
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("sale_price", serializer.errors)

    def test_owner_is_read_only(self):
        data = self.valid_payload()
        data["owner"] = self.other_user.pk

        serializer = ProductSerializer(data=data)

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        self.assertNotIn(
            "owner",
            serializer.validated_data
        )

class ProductAPITests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(
            username="owner",
            password="owner-pass-123!"
        )

        cls.other_user = User.objects.create_user(
            username="other",
            password="other-pass-123!"
        )

        cls.product = Product.objects.create(
            name="Keyboard",
            description="Mechanical keyboard",
            price="100.00",
            sale_price="80.00",
            stock=5,
            owner=cls.owner
        )

        cls.other_product = Product.objects.create(
            name="Mouse",
            description="Wireless mouse",
            price="50.00",
            sale_price="40.00",
            stock=10,
            owner=cls.other_user
        )

    def setUp(self):
        self.client.force_authenticate(user=self.owner)

    def product_payload(self):
        return {
            "name": "Monitor",
            "description": "27-inch monitor",
            "price": "300.00",
            "sale_price": "250.00",
            "stock": 10,
            "is_active": True,
        }

    def test_list_returns_only_own_products(self):
        response = self.client.get(
            reverse("product-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["id"],
            self.product.id
        )

    def test_create_assigns_authenticated_owner(self):
        payload = self.product_payload()
        payload["owner"] = self.other_user.id

        response = self.client.post(
            reverse("product-list"),
            payload,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        product = Product.objects.get(name="Monitor")

        self.assertEqual(
            product.owner_id,
            self.owner.id
        )

    def test_cannot_retrieve_another_users_product(self):
        response = self.client.get(
            reverse(
                "product-detail",
                args=[self.other_product.id]
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )

    def test_patch_updates_own_product(self):
        response = self.client.patch(
            reverse(
                "product-detail",
                args=[self.product.id]
            ),
            {"stock": 7},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 7)

    def test_delete_own_product(self):
        response = self.client.delete(
            reverse(
                "product-detail",
                args=[self.product.id]
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Product.objects.filter(
                pk=self.product.id
            ).exists()
        )

    def test_anonymous_client_cannot_list_products(self):
        client = APIClient()

        response = client.get(
            reverse("product-list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_token_endpoint_returns_token(self):
        client = APIClient()

        response = client.post(
            reverse("api_token_auth"),
            {
                "username": "owner",
                "password": "owner-pass-123!",
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertIn("token", response.data)