from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(HotelPhoto)
admin.site.register(HotelContact)
admin.site.register(HotelRoomType)
admin.site.register(HotelRoom)
admin.site.register(HotelRoomExtension)
admin.site.register(HotelRoomPhoto)
admin.site.register(HotelRoomReservation)