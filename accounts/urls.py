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
    path("hotel/get/", GetHotelInformationView.as_view(), name="get_hotel_information")
]