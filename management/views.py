from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
import json
from django.http import Http404

# Create your views here.

class ManageHotelContactView(APIView):

	serializer_class   = HotelContactSerializer
	permission_classes = [IsAuthenticated]


	def get_object(self, id):

		if HotelContact.objects.filter(id=id).exists():
			return HotelContact.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query      = HotelContact.objects.filter(hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		if "contact_type" not in request.data or "content" not in request.data:
			return Response("Invalid information", status=400)

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(hotel=request.user.hotel)

		return Response("Contact Created Successfully", status=201)

	def put(self, request, id):

		if self.get_object(id=id) == Http404:
			return Response('Object Not Found', status=404)

		if self.get_object(id=id).hotel != request.user.hotel:
			return Response('Bad Request', status=400)

		contact    = self.get_object(id=id)
		serializer = self.serializer_class(contact, data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response("Contact Updated Successfully", status=200)

	def delete(self, request, id):

		if self.get_object(id=id) == Http404:
			return Response('Object Not Found', status=404)

		if self.get_object(id=id).hotel.user != request.user:
			return Response('Bad Request', status=400)

		self.get_object(id=id).delete()

		return Response('Contact Deleted Successfully', status=200)

class ManageHotelPhoto(APIView):

	serializer_class   = HotelPhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self, id):

		if HotelPhoto.objects.filter(id=id).exists():
			return HotelPhoto.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query = HotelPhoto.objects.filter(hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(hotel=request.user.hotel)

		return Response("Photo Saved Successfully", status=201)

	def delete(self, request, id):

		photo = self.get_object(id=id)

		if photo == Http404:
			return Response('Object Not Found', status=404)

		if photo.hotel != request.user.hotel:
			return Response('Bad Request', status=400)

		photo.delete()

		return Response("Photo Deleted Successfully", status=200)

class ManageHotelRoomType(APIView):

	serializer_class   = HotelRoomTypeSerializer
	permission_classes = [IsAuthenticated]

	def get_object(self, id):

		if HotelRoomType.objects.filter(id=id).exists():
			return HotelRoomType.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query = HotelRoomType.objects.filter(hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(hotel=request.user.hotel)

		return Response("Hotel Room Type Created Successfully", status=201)

	def delete(self, request, id):

		hotel_room_type = self.get_object(id=id)

		if hotel_room_type == Http404:
			return Response('Object Not Found', status=404)

		if hotel_room_type.hotel != request.user.hotel:
			return Response('Bad Request', status=400)

		hotel_room_type.delete()

		return Response("Hotel Room Type Deleted Successfully", status=200)


class ManageHotelRoom(APIView):

	serializer_class   = HotelRoomSerializer
	permission_classes = [IsAuthenticated]

	def get_hotel_room_object(self, id):

		if HotelRoom.objects.filter(id=id).exists():
			return HotelRoom.objects.get(id=id)

		return Http404

	def get_hotel_room_type_object(self, id):

		if HotelRoomType.objects.filter(id=id).exists():
			return HotelRoomType.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query      = HotelRoom.objects.filter(room_type__hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		hotel_room_type = self.get_hotel_room_type_object(id=request.data.get('room_type'))

		if hotel_room_type == Http404:
			return Response("Object Not Found", status=404)

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(room_type=hotel_room_type)

		return Response("Room Saved Successfully", status=201)

	def delete(self, request, id):

		room = self.get_hotel_room_object(id=id)

		if room == Http404:
			return Response("Object Not Found", status=404)

		if room.room_type.hotel != request.user.hotel:
			return Response("Bad Request", status=400)

		room.delete()

		return Response("Room Deleted Successfully", status=200)


class ManageHotelRoomPhoto(APIView):

	serializer_class   = HotelRoomPhotoSerializer
	permission_classes = [IsAuthenticated]

	def get_hotel_room_photo_object(self, id):

		if HotelRoomPhoto.objects.filter(id=id).exists():
			return HotelRoomPhoto.objects.get(id=id)

		return Http404

	def get_hotel_room_object(self, id):

		if HotelRoom.objects.filter(id=id).exists():
			return HotelRoom.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query      = HotelRoomPhoto.objects.filter(room__room_type__hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		room = self.get_hotel_room_object(request.data.get('room'))

		if room == Http404:
			return Response("Object Not Found", status=404)

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(room=room)

		return Response("Room Photo Saved Successfully", status=201)

	def delete(self, request, id):

		photo = self.get_hotel_room_photo_object(id=id)

		if photo == Http404:
			return Response('Photo Not Found', status=404)

		if photo.room.room_type.hotel != request.user.hotel:
			return Response('Bad Request', status=400)

		photo.delete()

		return Response("Room Photo Deleted Successfully", status=200)

class ManageHotelRoomExtension(APIView):

	serializer_class   = HotelRoomExtensionSerializer
	permission_classes = [IsAuthenticated]

	def get_hotel_room_extension_object(self, id):

		if HotelRoomExtension.objects.filter(id=id).exists():
			return HotelRoomExtension.objects.get(id=id)

		return Http404

	def get_hotel_room_object(self, id):

		if HotelRoom.objects.filter(id=id).exists():
			return HotelRoom.objects.get(id=id)

		return Http404

	def get(self, request, id):

		query      = HotelRoomExtension.objects.filter(room__room_type__hotel=request.user.hotel)
		serializer = self.serializer_class(query, many=True)

		return Response(serializer.data, status=200)

	def post(self, request, id):

		room = self.get_hotel_room_object(request.data.get('room'))

		if room == Http404:
			return Response("Object Not Found", status=404)

		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save(room=room)

		return Response("Room Extension Created Successfully", status=201)

	def delete(self, request, id):

		extension = self.get_hotel_room_extension_object(id=id)

		if extension == Http404:
			return Response('Extension Not Found', status=404)

		if extension.room.room_type.hotel != request.user.hotel:
			return Response('Bad Request', status=400)

		extension.delete()

		return Response("Room Extension Deleted Successfully", status=200)