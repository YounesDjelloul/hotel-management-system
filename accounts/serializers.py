from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):

	id         = serializers.IntegerField(read_only=True)
	password1  = serializers.CharField(write_only=True)
	password2  = serializers.CharField(write_only=True)

	class Meta:
		model  = User
		fields = ['id', 'email', 'password1', 'password2']

	def validate(self, attrs):

		email     = attrs.get('email')
		password1 = attrs.get('password1')
		password2 = attrs.get('password2')

		if not email or not password1 or not password2:
			raise serializers.ValidationError('Invalid information.')

		if password1 != password2:
			raise serializers.ValidationError('Passwords didn\'t match')

		attrs['password'] = password1
		del attrs['password1']
		del attrs['password2']

		return attrs

	def create(self, validated_data):
		return User.objects.create_user(**validated_data)

class HotelSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only=True)

	class Meta:
		model  = Hotel
		fields = ['id', 'name', 'stars', 'lat', 'lng', 'description']

	def validate(self, attrs):

		hotel       = self.instance
		name        = attrs.get('name')
		stars       = attrs.get('stars')
		lat         = attrs.get('lat')
		lng         = attrs.get('lng')
		description = attrs.get('description')

		if hotel.name and name == "" or hotel.stars and stars == "" or hotel.lat and lat == "" or hotel.lng and lng == "" or hotel.description and description == "":
			raise serializers.ValidationError('Invalid information.')

		return attrs

	def create(self, validated_data):
		user = validated_data.pop('user')
		return Hotel.objects.filter(user=user).update(**validated_data)

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