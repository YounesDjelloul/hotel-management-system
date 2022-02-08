from django.urls import path
from .views import *

urlpatterns = [
    path('hotel/contact/<id>/', ManageHotelContactView.as_view(), name="manage_hotel_contact"),
    path('hotel/photo/<id>/', ManageHotelPhoto.as_view(), name="manage_hotel_photo"),
    path('hotel/room/type/<id>/', ManageHotelRoomType.as_view(), name="manage_hotel_room_type"),
    path('hotel/room/<id>/', ManageHotelRoom.as_view(), name="manage_hotel_room"),
    path('hotel/room/photo/<id>/', ManageHotelRoomPhoto.as_view(), name="manage_hotel_room_photo"),
    path('hotel/room/extension/<id>/', ManageHotelRoomExtension.as_view(), name="manage_hotel_room_extension"),
]