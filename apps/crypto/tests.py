from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model


class CryptoAPITestCase(APITestCase):
    client = APIClient()

    def setUp(self):
        self.valid_user_data = {
            "email": "test@gmail.com",
            "password": "Testing@1234",
            "confirm_password": "Testing@1234",
            "first_name": "Test",
            "last_name": "user",
        }
        User = get_user_model()
        self.user = User.objects.create_user(
            email=self.valid_user_data["email"],
            username="Testinguser",
            password=self.valid_user_data["password"],
            first_name=self.valid_user_data["first_name"],
            last_name=self.valid_user_data["last_name"],
        )
        self.response = self.client.post(
            reverse("login_v1"),
            data={
                "email": self.valid_user_data["email"],
                "password": self.valid_user_data["password"],
            },
        )

    def test_coin_list_view(self):
        response = self.client.get(reverse("coin_list_v1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coin_categories_view(self):
        response = self.client.get(reverse("coins_categories_v1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_coin_market_view(self):
        response = self.client.get(reverse("coin_market_v1"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
