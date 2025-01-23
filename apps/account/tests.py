from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class AccountModuleAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse("register_v1")
        self.valid_user_data = {
            "email": "test@gmail.com",
            "password": "Testing@1234",
            "confirm_password": "Testing@1234",
            "first_name": "Test",
            "last_name": "user",
        }
        self.invalid_user_data = {
            "email": "test@example.com",
            "password": "123456",
            "fullname": "Invalid User",
        }

    def test_signup_success(self):
        """Test user signup with valid data."""
        response = self.client.post(self.signup_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["status"])
        self.assertIn("User Creation Successfull", response.data["message"])

    def test_login_success(self):
        """Test user login with valid credentials."""
        User = get_user_model()
        self.user = User.objects.create_user(
            email=self.valid_user_data["email"],
            username="Testinguser",
            password=self.valid_user_data["password"],
            first_name=self.valid_user_data["first_name"],
            last_name=self.valid_user_data["last_name"],
        )
        response = self.client.post(
            reverse("login_v1"),
            data={
                "email": self.valid_user_data["email"],
                "password": self.valid_user_data["password"],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("token", response.data["data"])
