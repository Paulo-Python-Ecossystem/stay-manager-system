from django.contrib import admin
from .models.property import Hotel, Amenity
from .models.room import RoomType, Room
from .models.guest import Guest
from .models.booking import Booking, Payment

# Register your models here.


admin.site.register(Hotel)
admin.site.register(Amenity)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Guest)
admin.site.register(Booking)
admin.site.register(Payment)
