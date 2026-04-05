import jwt

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models.user import User, Account
from .models.permission import Role


class AuthenticationTests(APITestCase):

    def setUp(self):
        # Create a Role
        self.staff_role = Role.objects.create(label="Test Staff", is_staff=True)
        # Create User
        self.user = User.objects.create_user(username="staffuser", email="staff@test.com", password="testpassword123")
        # Create Account wrapper
        self.account = Account.objects.create(user=self.user, role=self.staff_role)

    def test_get_token(self):
        """
        Verify that hitting the token endpoint returns access/refresh tokens.
        """
        url = reverse("token_obtain_pair")
        data = {"username": "staffuser", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_token_payload_contains_role(self):
        """
        Verify that the custom token serializer adds 'role' and 'is_staff_role' correctly.
        """
        url = reverse("token_obtain_pair")
        data = {"username": "staffuser", "password": "testpassword123"}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        decoded_payload = jwt.decode(response.data["access"], options={"verify_signature": False})

        self.assertIn("role", decoded_payload)
        self.assertEqual(decoded_payload["role"], "Test Staff")
        self.assertIn("is_staff_role", decoded_payload)
        self.assertTrue(decoded_payload["is_staff_role"])
