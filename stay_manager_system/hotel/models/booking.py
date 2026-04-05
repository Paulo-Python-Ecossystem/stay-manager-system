from django.db import models

from .guest import Guest
from .room import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CHECKED_IN", "Checked In"),
        ("CHECKED_OUT", "Checked Out"),
        ("CANCELLED", "Cancelled"),
    ]

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    guest = models.ForeignKey(Guest, on_delete=models.CASCADE, related_name="bookings", verbose_name="Guest")
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name="bookings", verbose_name="Room")

    check_in_date = models.DateField(verbose_name="Check-in Date")
    check_out_date = models.DateField(verbose_name="Check-out Date")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Status")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")

    created_by = models.ForeignKey(
        "hotel_auth.Account",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="created_bookings",
        verbose_name="Created By Staff",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.guest} - {self.room}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("CASH", "Cash"),
        ("CREDIT_CARD", "Credit Card"),
        ("BANK_TRANSFER", "Bank Transfer"),
        ("OTHER", "Other"),
    ]

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("REFUNDED", "Refunded"),
    ]

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments", verbose_name="Booking")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Payment Method")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING", verbose_name="Status")
    transaction_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction ID")

    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Payment Date")

    def __str__(self):
        return f"Payment {self.id} for Booking {self.booking.id} - {self.amount}"
