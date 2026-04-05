from hotel_auth.permissions import HasRole, IsStaffRole
from rest_framework import permissions, viewsets

from .models.booking import Booking, Payment
from .models.guest import Guest
from .models.property import Amenity, Hotel
from .models.room import Room, RoomType

from .serializers import (
    AmenitySerializer,
    BookingSerializer,
    GuestSerializer,
    HotelSerializer,
    PaymentSerializer,
    RoomSerializer,
    RoomTypeSerializer,
)


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsStaffRole]
    filterset_fields = ["name"]
    search_fields = ["name", "address", "description"]
    ordering_fields = ["name", "created_at"]


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializer
    permission_classes = [IsStaffRole]
    search_fields = ["name"]


class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
    permission_classes = [IsStaffRole]
    filterset_fields = ["capacity"]
    search_fields = ["name", "description"]
    ordering_fields = ["base_price", "capacity"]


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["hotel", "room_type", "status", "floor"]
    search_fields = ["room_number", "floor"]
    ordering_fields = ["room_number", "hotel"]


class GuestViewSet(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["user", "identification_type"]
    search_fields = ["first_name", "last_name", "email", "identification_number"]
    ordering_fields = ["first_name", "last_name", "created_at"]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["guest", "room", "status", "room__hotel"]
    search_fields = ["guest__first_name", "guest__last_name"]
    ordering_fields = ["check_in_date", "check_out_date", "created_at"]

    def perform_create(self, serializer):
        if hasattr(self.request.user, "account"):
            booking = serializer.save(created_by=self.request.user.account)
        else:
            booking = serializer.save()

        # Trigger confirmation email asynchronously
        from .tasks import send_booking_confirmation_email

        guest_email = booking.guest.email
        guest_name = str(booking.guest)

        # fallback email to user if not on guest profile
        if not guest_email and booking.guest.user:
            guest_email = booking.guest.user.email

        if guest_email:
            send_booking_confirmation_email.delay(
                booking_id=booking.id,
                guest_email=guest_email,
                guest_name=guest_name,
                room_number=booking.room.room_number,
                hotel_name=booking.room.hotel.name,
                check_in=str(booking.check_in_date),
                check_out=str(booking.check_out_date),
            )


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["booking", "payment_method", "status"]
    ordering_fields = ["payment_date", "amount"]
