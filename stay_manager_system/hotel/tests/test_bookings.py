from datetime import date, timedelta
from unittest.mock import patch

from django.urls import reverse
from hotel.models.booking import Booking
from hotel.models.guest import Guest
from hotel.models.property import Hotel
from hotel_auth.models.user import User
from hotel.models.room import Room, RoomType
from rest_framework import status
from rest_framework.test import APITestCase


class BookingTests(APITestCase):

    def setUp(self):
        # Setup basic data required to create a booking
        self.user = User.objects.create_user(username="booker", email="booker@test.com", password="123")
        self.client.force_authenticate(user=self.user)

        self.hotel = Hotel.objects.create(name="Test Hotel", address="123 Test St", email="contact@testhotel.com")
        self.room_type = RoomType.objects.create(name="Suite", capacity=2, base_price=100.00)
        self.room = Room.objects.create(hotel=self.hotel, room_type=self.room_type, room_number="101")
        self.guest = Guest.objects.create(
            user=self.user,
            first_name="John",
            last_name="Doe",
            email="booker@test.com",
        )

    @patch("hotel.tasks.send_booking_confirmation_email.delay")
    def test_create_booking_triggers_celery_task(self, mock_delay):
        """
        Test that creating a booking via the API triggers the confirmation email celery task.
        """
        url = reverse("booking-list")
        check_in = date.today()
        check_out = check_in + timedelta(days=2)

        payload = {
            "guest": self.guest.id,
            "room": self.room.id,
            "check_in_date": str(check_in),
            "check_out_date": str(check_out),
            "total_price": "200.00",
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

        # Verify if the delayed task was triggered
        booking = Booking.objects.first()
        mock_delay.assert_called_once_with(
            booking_id=booking.id,
            guest_email=self.guest.email,
            guest_name=str(self.guest),
            room_number=self.room.room_number,
            hotel_name=self.hotel.name,
            check_in=str(booking.check_in_date),
            check_out=str(booking.check_out_date),
        )
