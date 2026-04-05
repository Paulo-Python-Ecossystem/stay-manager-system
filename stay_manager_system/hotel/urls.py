from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"hotels", views.HotelViewSet)
router.register(r"amenities", views.AmenityViewSet)
router.register(r"room-types", views.RoomTypeViewSet)
router.register(r"rooms", views.RoomViewSet)
router.register(r"guests", views.GuestViewSet)
router.register(r"bookings", views.BookingViewSet)
router.register(r"payments", views.PaymentViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
]
