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

		if name == "" or stars == "" or lat == "" or lng == "" or description == "":
			raise serializers.ValidationError('Invalid information.')

		return attrs

	def create(self, validated_data):
		user = validated_data.pop('user')
		return Hotel.objects.filter(user=user).update(**validated_data)