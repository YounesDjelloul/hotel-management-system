from django.urls import path
from .views import *

urlpatterns = [
    path('intent/create/', CreatePaymentIntentView.as_view(), name="create_payment_intent"),
]