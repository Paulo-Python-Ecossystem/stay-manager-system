from django.contrib import admin
from hotel.models.property import Hotel, Amenity
from hotel.models.room import RoomType, Room
from hotel.models.guest import Guest
from hotel.models.booking import Booking, Payment
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Payment)
