from django.urls import reverse
from hotel_auth.models.permission import Role
from hotel_auth.models.user import User, Account
from rest_framework import status
from rest_framework.test import APITestCase



class ApiPermissionsTests(APITestCase):

    def setUp(self):
        # Create Staff User
        self.staff_role = Role.objects.create(label="Staff", is_staff=True)
        self.staff_user = User.objects.create_user(username="staff", password="123")
        Account.objects.create(user=self.staff_user, role=self.staff_role)

        # Create Regular User
        self.regular_role = Role.objects.create(label="Guest", is_staff=False)
        self.regular_user = User.objects.create_user(username="guest", password="123")
        Account.objects.create(user=self.regular_user, role=self.regular_role)

    def test_unauthenticated_access_is_forbidden(self):
        """
        Unauthenticated users cannot access the API.
        """
        url = reverse("room-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_staff_can_access_protected_endpoints(self):
        """
        Staff uses HotelViewSet which has IsStaffRole permission.
        """
        url = reverse("hotel-list")
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(url)
        # Should be able to list hotels
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_cannot_access_staff_endpoints(self):
        """
        A regular guest cannot access hotel management endpoints.
        """
        url = reverse("hotel-list")
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.get(url)
        # Assuming IsStaffRole returns Forbidden explicitly.
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
