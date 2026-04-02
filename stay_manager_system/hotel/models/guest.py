from django.db import models
from django.conf import settings

class Guest(models.Model):
    class Meta:
        verbose_name = "Guest"
        verbose_name_plural = "Guests"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True, 
        related_name="guest_profile", 
        verbose_name="User"
    )
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Phone Number")
    
    IDENTIFICATION_CHOICES = [
        ('PASSPORT', 'Passport'),
        ('NATIONAL_ID', 'National ID'),
        ('DRIVER_LICENSE', 'Driver License'),
        ('OTHER', 'Other'),
    ]
    identification_type = models.CharField(max_length=20, choices=IDENTIFICATION_CHOICES, blank=True, null=True, verbose_name="ID Type")
    identification_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID Number")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        if self.user:
            return self.user.get_full_name() or self.user.username
        return f"Guest {self.id}"
