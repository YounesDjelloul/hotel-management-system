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
class TestUpdateHotelInformation:

	def test_update_hotel_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()

		url  = reverse('update_hotel_information')
		data = {

			"name": "EL DJAZAIR",
		}

		response = client.post(url, data, **headers)

		print(Hotel.objects.all())

		assert response.status_code == 202
		assert Hotel.objects.get(id=1).name == "EL DJAZAIR"

@pytest.mark.django_db
class TestManageHotelContact:

	def test_get_all_created_contacts(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		contact = HotelContact.objects.create(hotel=user.hotel, contact_type='email', content="younes@gm.com")

		url     = reverse('manage_hotel_contact', kwargs={"id": None})

		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_new_contact_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_contact', kwargs={"id": None})

		data    = {

			"contact_type": "email",
			"content": "younesdjelloul14@gmail.com"
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelContact.objects.get(id=1).contact_type == "email"
		assert HotelContact.objects.get(id=1).content == "younesdjelloul14@gmail.com"

	def test_create_new_contact_with_invalid_information(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_contact', kwargs={"id": None})

		data    = {

			"content": "younesdjelloul14@gmail.com"
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_update_existing_contact(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		contact = HotelContact.objects.create(hotel=user.hotel, contact_type='email', content="younes@gm.com")

		url     = reverse('manage_hotel_contact', kwargs={"id": contact.id})

		data    = {

			"content": "younesdjelloul@gm.com"
		}

		response = client.put(url, data, content_type='application/json', **headers)

		assert response.status_code == 200
		assert HotelContact.objects.get(id=contact.id).content == "younesdjelloul@gm.com"

	def test_update_existing_contact_with_invalid_information(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		contact = HotelContact.objects.create(hotel=user.hotel, contact_type='email', content="younes@gm.com")

		url     = reverse('manage_hotel_contact', kwargs={"id": contact.id})

		data    = {

			# content is missing
		}

		response = client.put(url, data, content_type='application/json', **headers)

		assert response.status_code == 400

	def test_delete_existing_contact_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		contact = HotelContact.objects.create(hotel=user.hotel, contact_type='email', content="younes@gm.com")

		url     = reverse('manage_hotel_contact', kwargs={"id": contact.id})

		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelContact.objects.filter(id=contact.id).exists() == False


class TestManageHotelPhoto:

	def test_get_all_existing_photos(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		photo   = HotelPhoto.objects.create(hotel=user.hotel, photo="https://aws.amazon.com/156596/")
		
		url     = reverse('manage_hotel_photo', kwargs={"id": None})

		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_new_hotel_photo_with_valid_data(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_photo', kwargs={"id": None})

		data    = {

			"photo": "https://aws.amazon.com/156596/"
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelPhoto.objects.get(id=1).photo == "https://aws.amazon.com/156596/"

	def test_create_new_hotel_photo_with_invalid_data(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_photo', kwargs={"id": None})

		data    = {

			# photo url is missing
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_delete_existing_photos(self, client, get_login_headers):

		headers = get_login_headers()
		user    = User.objects.get(email="younes@dj.com")
		photo   = HotelPhoto.objects.create(hotel=user.hotel, photo="https://aws.amazon.com/156596/")
		
		url     = reverse('manage_hotel_photo', kwargs={"id": photo.id})

		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelPhoto.objects.filter(photo="https://aws.amazon.com/156596/").exists() == False

@pytest.mark.django_db
class TestManageHotelRoomType:

	def test_get_all_existing_hotel_room_type(self, client, get_login_headers):

		headers = get_login_headers()
		
		user            = User.objects.get(id=1)
		hotel_room_type = HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

		url      = reverse("manage_hotel_room_type", kwargs={"id": None})

		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_hotel_room_type_with_invalid_information(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_room_type', kwargs={"id": None})

		data    = {

			#"room_type": "Single" # room_type is missing
			"price": 140.00
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_create_hotel_room_type_with_valid_information(self, client, get_login_headers):

		headers = get_login_headers()
		url     = reverse('manage_hotel_room_type', kwargs={"id": None})

		data    = {

			"room_type": "single", # room_type is not missing
			"price": 140.00
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelRoomType.objects.get(id=1).room_type == "single"
		assert HotelRoomType.objects.get(id=1).price == 140.00

	def test_delete_hotel_room_type(self, client, get_login_headers):

		headers         = get_login_headers()
		user            = User.objects.get(id=1)
		hotel_room_type = HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

		url      = reverse("manage_hotel_room_type", kwargs={"id": hotel_room_type.id})

		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelRoomType.objects.filter(id=1).exists() == False


@pytest.mark.django_db
class TestManageHotelRoom:

	def create_room_type(self):
		user = User.objects.get(id=1)
		return HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

	def test_get_all_hotel_rooms(self, client, get_login_headers):

		headers         = get_login_headers()
		hotel_room_type = self.create_room_type()
		room            = HotelRoom.objects.create(room_type=hotel_room_type, title="Hello Title", description="Hello Desc", room_number=102)

		url      = reverse('manage_hotel_room', kwargs={"id": None})
		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_new_hotel_room_with_valid_information(self, client, get_login_headers):

		headers         = get_login_headers()
		hotel_room_type = self.create_room_type()

		url      = reverse('manage_hotel_room', kwargs={"id": None})
		data     = {

			"room_type": hotel_room_type.id,
			"title": "Hello Title", # title is not missing
			"description": "Hello Desc",
			"room_number": 104
		}
		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelRoom.objects.get(id=1).title == "Hello Title"

	def test_create_new_hotel_room_with_invalid_information(self, client, get_login_headers):

		headers         = get_login_headers()
		hotel_room_type = self.create_room_type()

		url      = reverse('manage_hotel_room', kwargs={"id": None})
		data     = {

			"room_type": hotel_room_type.id,
			# "title": "Hello Title", # title is missing
			"description": "Hello Desc",
			"room_number": 104
		}
		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_delete_hotel_room(self, client, get_login_headers):

		headers         = get_login_headers()
		hotel_room_type = self.create_room_type()
		room            = HotelRoom.objects.create(room_type=hotel_room_type, title="Hello Title", description="Hello Desc", room_number=102)

		url      = reverse('manage_hotel_room', kwargs={"id": room.id})
		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelRoom.objects.filter(id=1).exists() == False

class TestManageHotelRoomPhoto:

	def create_room(self):

		user            = User.objects.get(id=1)
		hotel_room_type = HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

		return HotelRoom.objects.create(room_type=hotel_room_type, title="Hello Title", description="Hello Desc", room_number=102)

	def test_get_all_existing_photos(self, client, get_login_headers):

		headers = get_login_headers()
		room    = self.create_room()
		photo   = HotelRoomPhoto.objects.create(room=room, photo="https://aws.amazon.com/156596/")
		
		url     = reverse('manage_hotel_room_photo', kwargs={"id": None})

		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_new_hotel_room_photo_with_valid_data(self, client, get_login_headers):

		headers = get_login_headers()
		self.create_room()
		url     = reverse('manage_hotel_room_photo', kwargs={"id": None})

		data    = {

			"room": 1,
			"photo": "https://aws.amazon.com/156596/"
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelRoomPhoto.objects.get(id=1).photo == "https://aws.amazon.com/156596/"

	def test_create_new_hotel_room_photo_with_invalid_data(self, client, get_login_headers):

		headers = get_login_headers()
		self.create_room()
		url     = reverse('manage_hotel_room_photo', kwargs={"id": None})

		data    = {

			"room": 1
			# photo url is missing
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_delete_existing_photos(self, client, get_login_headers):

		headers = get_login_headers()
		room    = self.create_room()
		photo   = HotelRoomPhoto.objects.create(room=room, photo="https://aws.amazon.com/156596/")
		
		url     = reverse('manage_hotel_room_photo', kwargs={"id": photo.id})

		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelRoomPhoto.objects.filter(photo="https://aws.amazon.com/156596/").exists() == False


class TestManageHotelRoomExtension:

	def create_room(self):

		user            = User.objects.get(id=1)
		hotel_room_type = HotelRoomType.objects.create(hotel=user.hotel, room_type="Single", price=140.00)

		return HotelRoom.objects.create(room_type=hotel_room_type, title="Hello Title", description="Hello Desc", room_number=102)

	def test_get_all_existing_extensions(self, client, get_login_headers):

		headers   = get_login_headers()
		room      = self.create_room()
		extension = HotelRoomExtension.objects.create(room=room, content="Food")
		
		url     = reverse('manage_hotel_room_extension', kwargs={"id": None})

		response = client.get(url, **headers)

		assert response.status_code == 200

	def test_create_new_hotel_room_photo_with_valid_data(self, client, get_login_headers):

		headers = get_login_headers()
		self.create_room()
		url     = reverse('manage_hotel_room_extension', kwargs={"id": None})

		data    = {

			"room": 1,
			"content": "Food"
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 201
		assert HotelRoomExtension.objects.get(id=1).content == "Food"

	def test_create_new_hotel_room_extension_with_invalid_data(self, client, get_login_headers):

		headers = get_login_headers()
		self.create_room()
		url     = reverse('manage_hotel_room_extension', kwargs={"id": None})

		data    = {

			"room": 1
			# content url is missing
		}

		response = client.post(url, data, **headers)

		assert response.status_code == 400

	def test_delete_existing_extensions(self, client, get_login_headers):

		headers   = get_login_headers()
		room      = self.create_room()
		extension = HotelRoomExtension.objects.create(room=room, content="Food")
		
		url     = reverse('manage_hotel_room_extension', kwargs={"id": extension.id})

		response = client.delete(url, **headers)

		assert response.status_code == 200
		assert HotelRoomExtension.objects.filter(content="Food").exists() == False
