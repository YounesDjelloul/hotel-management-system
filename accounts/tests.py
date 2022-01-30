import pytest
from django.urls import reverse
from .models import *

# Create your tests here.

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