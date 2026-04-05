from django.db import models
from .property import Hotel, Amenity


class RoomType(models.Model):
    class Meta:
        verbose_name = "Room Type"
        verbose_name_plural = "Room Types"

    name = models.CharField(max_length=100, verbose_name="Type Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Price per Night")
    capacity = models.PositiveIntegerField(default=1, verbose_name="Capacity")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="room_types", verbose_name="Amenities")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - Capacity: {self.capacity}"


class Room(models.Model):
    ROOM_STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
        ("CLEANING", "Cleaning"),
        ("MAINTENANCE", "Needs Maintenance"),
    ]

    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        unique_together = ('hotel', 'room_number')

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms", verbose_name="Hotel")
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name="rooms", verbose_name="Room Type")
    room_number = models.CharField(max_length=20, verbose_name="Room Number")
    floor = models.CharField(max_length=20, blank=True, null=True, verbose_name="Floor")
    status = models.CharField(max_length=20, choices=ROOM_STATUS_CHOICES, default="AVAILABLE", verbose_name="Status")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Room {self.room_number} - {self.hotel.name}"
