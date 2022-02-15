import pytest
from django.urls import reverse
from django.core import mail
from .models import *
import json

# Create your tests here.

@pytest.fixture
def create_user(db):
	
	def make_user():

		user = User.objects.create_user(email="younes@dj.com", password="younes@@456", stripe_account="hfduhfuhsi,bjof")
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
		assert User.objects.all()[0].email == "younesdjelloul14@gmail.com"
		assert User.objects.all()[0].stripe_account != None
		assert User.objects.all()[0].hotel.name == None

@pytest.mark.django_db
class TestUpdateHotelInformation:

	def test_update_hotel_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()

		url  = reverse('manage_hotel_information')
		data = {

			"name": "EL DJAZAIR",
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 202
		assert Hotel.objects.get(id=1).name == "EL DJAZAIR"

	def test_update_hotel_with_invalid_information(self, client, get_login_headers):

		headers = get_login_headers()

		url  = reverse('manage_hotel_information')
		data = {

			"name": "",
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400
		assert Hotel.objects.get(id=1).name == None

@pytest.mark.django_db
class TestGetHotelInformation:

	def test_get_hotel_information(self, client, get_login_headers):

		headers = get_login_headers()

		url     = reverse("manage_hotel_information")

		response = client.get(url, **headers)

		assert response.status_code == 200
		assert len(mail.outbox) == 1

@pytest.mark.django_db
class TestActivateUser:

	def test_activate_user(self, client, get_login_headers):

		headers  = get_login_headers()
		url      = reverse('activate_user', kwargs={'id': User.objects.all()[0].id})

		response = client.get(url)

		assert response.status_code == 200

	def test_activate_user_with_invalid_information(self, client, get_login_headers):
		headers  = get_login_headers()
		url      = reverse('activate_user', kwargs={'id': 5})

		response = client.get(url)

		assert response.status_code == 400
		assert len(mail.outbox) == 0