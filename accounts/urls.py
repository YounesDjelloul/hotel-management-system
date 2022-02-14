from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    path('create/', CreateUserView.as_view(), name='create_user'),
    path('hotel/', ManageHotelInformationView.as_view(), name='manage_hotel_information'),
    path('activate/<id>/', ActivateUserView.as_view(), name="activate_user"),
]