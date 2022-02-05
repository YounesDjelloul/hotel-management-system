from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    path('user/create/', CreateUserView.as_view(), name='create_user'),
    path('hotel/update/', UpdateHotelInformationView.as_view(), name='update_hotel_information'),
    path('hotel/contact/<id>/', ManageHotelContactView.as_view(), name="manage_hotel_contact"),
    path('hotel/photo/<id>/', ManageHotelPhoto.as_view(), name="manage_hotel_photo"),
    path('hotel/room/type/<id>/', ManageHotelRoomType.as_view(), name="manage_hotel_room_type"),
    path('hotel/room/<id>/', ManageHotelRoom.as_view(), name="manage_hotel_room"),
    path('hotel/room/photo/<id>/', ManageHotelRoomPhoto.as_view(), name="manage_hotel_room_photo"),
    path('hotel/room/extension/<id>/', ManageHotelRoomExtension.as_view(), name="manage_hotel_room_extension"),

]