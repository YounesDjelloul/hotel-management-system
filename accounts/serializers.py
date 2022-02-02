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

		hotel       = self.instance.hotel
		name        = attrs.get('name')
		stars       = attrs.get('stars')
		lat         = attrs.get('lat')
		lng         = attrs.get('lng')
		description = attrs.get('description')

		if hotel.name and name == "" or hotel.stars and stars == "" or hotel.lat and lat == "" or hotel.lng and lng == "" or hotel.description and description == "":
			raise serializers.ValidationError('Invalid information.')

		return attrs

class HotelContactSerializer(serializers.ModelSerializer):

	id = serializers.IntegerField(read_only=True)

	class Meta:
		model  = HotelContact
		fields = ['id', 'contact_type', 'content']

	def validate(self, attrs):

		contact_type = attrs.get('contact_type')
		content      = attrs.get('content')

		if not contact_type or not content:
			raise serializers.ValidationError('Invalid information')

		return attrs

	def create(self, validated_data):
		return HotelContact.objects.create(**validated_data)