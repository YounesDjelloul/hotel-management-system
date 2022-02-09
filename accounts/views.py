from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json
from django.http import Http404
from payment.services import *

# Create your views here.

class CreateUserView(APIView):

	serializer_class = UserSerializer

	def post(self, request):

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(stripe_account=create_connected_account())

		return Response(serializer.data, status=201)

class UpdateHotelInformationView(APIView):

	serializer_class   = HotelSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):

		serializer = self.serializer_class(data=request.data, instance=request.user.hotel)
		serializer.is_valid(raise_exception=True)
		serializer.save(user=request.user)

		return Response("Information Updated Successfully", status=202)

class GetHotelInformationView(APIView):

	serializer_class   = HotelSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):

		query      = Hotel.objects.get(user=request.user)
		serializer = self.serializer_class(query)

		return Response(serializer.data, status=200)