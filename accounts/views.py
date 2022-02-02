from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json

# Create your views here.

class CreateUserView(APIView):

	serializer_class = UserSerializer

	def post(self, request):

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=201)

class EditHotelInformationView(APIView):

	serializer_class   = HotelSerializer
	permission_classes = [IsAuthenticated]

	def post(self, request):

		serializer = self.serializer_class(data=request.data, instance=request.user)
		serializer.is_valid(raise_exception=True)

		hotel = Hotel.objects.filter(user=request.user).update(**request.data)

		return Response("Information Updated Successfully", status=202)

class ManageHotelContactView(APIView):

	serializer_class   = HotelContactSerializer
	permission_classes = [IsAuthenticated]


	def get_object(self, id):

		try:
			return HotelContact.objects.filter(id=id)
		except HotelContact.DoesNotExist:
			return Http404

	def post(self, request):

		serializer = self.serializer_class(data=request.data, instance=request.user.hotel)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response("Contact Created Successfully", status=201)

	def put(self, request, id):

		if not self.get_object(id=id):
			return Response('Contact Not Found', status=404)

		contact    = self.get_object(id=id)
		serializer = self.serializer_class(data=request.data, instance=request.user.hotel)
		serializer.save()

		return Response('Contact Updated Successfully', status=200)

	def delete(self, request, id):

		if not self.get_object(id=id):
			return Response('Contact Not Found', status=404)

		if self.get_object(id=id).hotel.user != request.user:
			return Response('Bad Request', status=400)

		self.get_object(id=id).delete()

		return Response('Contact Deleted Successfully', status=200)