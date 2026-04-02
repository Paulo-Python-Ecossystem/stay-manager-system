from django.db import models

class Amenity(models.Model):
    class Meta:
        verbose_name = "Amenity"
        verbose_name_plural = "Amenities"

    name = models.CharField(max_length=100, unique=True, verbose_name="Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="CSS class or icon name")

    def __str__(self):
        return self.name

class Hotel(models.Model):
    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

    name = models.CharField(max_length=255, verbose_name="Name")
    address = models.TextField(verbose_name="Address")
    email = models.EmailField(verbose_name="Email", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="hotels", verbose_name="Amenities")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
