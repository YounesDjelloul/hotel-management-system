import pytest
from django.urls import reverse
from management.models import *
from accounts.models import *
from management.models import *
from payment.services import create_connected_account
import json

# Create your tests here.

@pytest.fixture
def create_user(db):
	
	def make_user():

		user = User.objects.create_user(email="younes@dj.com", password="younes@@456", stripe_account=create_connected_account())
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


class TestPaymentIntent:

	def setUp(self):

		user            = User.objects.get(id=1)
		hotel_room_type = HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

		return HotelRoom.objects.create(room_type=hotel_room_type, title="Hello Title", description="Hello Desc", room_number=102)

	def test_create_payment_intent(self, client, get_login_headers):

		headers  = get_login_headers()

		self.setUp()

		url      = reverse("create_payment_intent")
		data     = {

			"fullname": "Younes Djelloul",
			"check_in": "2022-01-22",
			"check_out": "2022-01-25",
			"phone_number": "05505654525",
			"room_number": 102
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelRoomReservation.objects.filter(id=1).exists() == True
		assert 'client_secret' in json.loads(response.content)