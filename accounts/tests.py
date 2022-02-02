import pytest
from django.urls import reverse
from .models import *
from rest_framework.test import APIClient
import json

# Create your tests here.

@pytest.fixture
def create_user(db):
	
	def make_user():

		user = User.objects.create_user(email="younes@dj.com", password="younes@@456")
		return user

	return make_user

@pytest.fixture
def get_login_headers(db, client, create_user):

	def auto_login_user():

		user = create_user()

		url  = reverse('obtain_token')
		data = {"email": user.email, "password": "younes@@456"}

		response = client.post(url, data, format='json')
		access   = response.json()['access']

		return {"HTTP_AUTHORIZATION": f'Bearer {access}'}

	return auto_login_user

@pytest.mark.django_db
class TestCreateHotel:

	def test_create_hotel_with_unmatched_passwords(self, client):

		url      = reverse('create_user')
		data     = {

			"email": "younesdjelloul14@gmail.com",
			"password1": "younes@@456",
			"password2": "younes456" # passwords didn't match
		}

		response = client.post(url, data, format='json')

		assert response.status_code == 400

	def test_create_hotel_with_no_email(self, client):

		url      = reverse('create_user')
		data     = {

			"password1": "younes@@456",
			"password2": "younes456" # passwords unmatched
		}

		response = client.post(url, data, format='json')

		assert response.status_code == 400

	def test_create_hotel_with_valid_information(self, client):

		url      = reverse('create_user')
		data     = {

			"email": "younesdjelloul14@gmail.com",
			"password1": "younes@@456",
			"password2": "younes@@456" # passwords matched
		}

		response = client.post(url, data, format='json')

		assert response.status_code == 201
		assert User.objects.get(id=1).email == "younesdjelloul14@gmail.com"
		assert User.objects.get(id=1).hotel.name == None

@pytest.mark.django_db
class TestFillHotelInformation:

	def test_fill_hotel_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()

		url  = reverse('edit_hotel_information')
		data = {

			"name": "EL DJAZAIR",
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 202
		assert Hotel.objects.get(id=1).name == "['EL DJAZAIR']"