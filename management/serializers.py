from rest_framework import serializers
from .models import *
from accounts.serializers import HotelSerializer

class HotelContactSerializer(serializers.ModelSerializer):

	id           = serializers.IntegerField(read_only=True)
	content      = serializers.CharField(required=False)
	contact_type = serializers.CharField(required=False)
	hotel        = HotelSerializer(read_only=True)

	class Meta:
		model  = HotelContact
		fields = ['id', 'hotel', 'contact_type', 'content']

	def validate(self, attrs):

		contact_type = attrs.get('contact_type')
		content      = attrs.get('content')

		if hasattr(self, "instance"):
			if not contact_type and not content or contact_type == "" and content == "":
				raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelContact.objects.create(**validated_data)

	def update(self, instance, validated_data):
		return HotelContact.objects.filter(id=instance.id).update(**validated_data)

class HotelPhotoSerializer(serializers.ModelSerializer):

	id     = serializers.IntegerField(read_only=True)
	hotel  = HotelSerializer(read_only=True)

	class Meta:
		model  = HotelPhoto
		fields = ['id', 'hotel', 'photo']

	def validate(self, attrs):

		photo = attrs.get('photo')

		if not photo:
			raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelPhoto.objects.create(**validated_data)

class HotelRoomTypeSerializer(serializers.ModelSerializer):

	id     = serializers.IntegerField(read_only=True)
	hotel  = HotelSerializer(read_only=True)

	class Meta:
		model  = HotelRoomType
		fields = ['id', 'hotel', 'room_type', 'price']

	def validate(self, attrs):

		room_type = attrs.get('room_type')
		price     = attrs.get('price')

		if not room_type or not price:
			raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelRoomType.objects.create(**validated_data)

class HotelRoomSerializer(serializers.ModelSerializer):

	id        = serializers.IntegerField(read_only=True)
	room_type = HotelRoomTypeSerializer(read_only=True)

	class Meta:
		model  = HotelRoom
		fields = ['id', 'room_type', 'title', 'description', 'room_number']

	def validate(self, attrs):

		title       = attrs.get('title')
		description = attrs.get('description')
		room_number = attrs.get('room_number')

		if not title or not description or not room_number:
			raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelRoom.objects.create(**validated_data)

class HotelRoomPhotoSerializer(serializers.ModelSerializer):

	id    = serializers.IntegerField(read_only=True)
	room  = HotelRoomSerializer(read_only=True)

	class Meta:
		model  = HotelRoomPhoto
		fields = ['id', 'room', 'photo']

	def validate(self, attrs):

		photo = attrs.get('photo')

		if not photo:
			raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelRoomPhoto.objects.create(**validated_data)

class HotelRoomExtensionSerializer(serializers.ModelSerializer):

	id    = serializers.IntegerField(read_only=True)
	room  = HotelRoomSerializer(read_only=True)

	class Meta:
		model  = HotelRoomExtension
		fields = ['id', 'room', 'content']

	def validate(self, attrs):

		content = attrs.get('content')

		if not content:
			raise serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelRoomExtension.objects.create(**validated_data)

class ReservationSerializer(serializers.ModelSerializer):

	total_price = serializers.IntegerField(read_only=True)
	qr_photo    = serializers.IntegerField(read_only=True)

	class Meta:
		model  = HotelRoomReservation
		fields = ['id', 'fullname', 'check_in', 'check_out', 'total_price', 'phone_number', 'room_number', 'qr_photo']

	def validate(self, attrs):

		fullname     = attrs.get('fullname')
		check_in     = attrs.get('check_in')
		check_out    = attrs.get('check_out')
		phone_number = attrs.get('phone_number')
		room_number  = attrs.get('room_number')

		if not fullname or not check_in or not check_in or not phone_number or not room_number:
			return serializers.ValidationError("Invalid information")

		return attrs

	def create(self, validated_data):
		return HotelRoomReservation.objects.create(**validated_data)