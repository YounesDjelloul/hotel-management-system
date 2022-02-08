from django.shortcuts import render
from rest_framework.views import APIView
from management.serializers import ReservationSerializer
from .services import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class CreatePaymentIntentView(APIView):

	serializer_class   = ReservationSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):

		serializer  = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		valid       = serializer.validated_data

		price       = get_room_price(room_number=valid.get('room_number'))
		total_price = calculate_reservation_total_price(valid.get('check_in'), valid.get('check_out'), price)

		serializer.save(total_price=total_price)

		payment_intent = create_payment_intent(

			amount=total_price,
			stripe_account=request.user.stripe_account
		)

		return Response({"client_secret": payment_intent.client_secret}, status=201)