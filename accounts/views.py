from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json
from django.http import Http404
from payment.services import *
from uuid import UUID

# Create your views here.

class CreateUserView(APIView):

	serializer_class = UserSerializer

	def post(self, request):

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(stripe_account=create_connected_account())

		return Response(serializer.data, status=201)

class ManageHotelInformationView(APIView):

	serializer_class   = HotelSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request):

		query      = Hotel.objects.get(user=request.user)
		serializer = self.serializer_class(query)

		return Response(serializer.data, status=200)

	def post(self, request):

		serializer = self.serializer_class(data=request.data, instance=request.user.hotel)
		serializer.is_valid(raise_exception=True)
		serializer.save(user=request.user)

		return Response("Information Updated Successfully", status=202)

class ActivateUserView(APIView):

	def get(self, request, id):

		id = id.replace('-', "")

		try:
			check = UUID(id, version=4)
		except ValueError:
			return Response('Invalid information ...', status=400)

		if not User.objects.filter(id=id).exists():
			return Response('Invalid information', status=400)

		user = User.objects.get(id=id)

		user.status = True
		user.save()

		return Response('User Activated Successfully', status=200)