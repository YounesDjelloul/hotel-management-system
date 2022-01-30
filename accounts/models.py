from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):

	def create_user(self, email, password):
		if email and password:
			user = User(email=email)
			user.set_password(password)
			user.save()

			return user

	def create_superuser(self, email, password):
		if email and password:
			user = User(email=email, is_superuser=True, is_staff=True)
			user.set_password(password)
			user.save()

			return user

class User(AbstractUser):

	first_name = None
	last_name  = None
	username   = None

	email      = models.EmailField(unique=True)

	USERNAME_FIELD  = 'email'
	REQUIRED_FIELDS = []
	objects         = UserManager()

	def __str__(self):
		return str(self.email)


class Hotel(models.Model):

	user        = models.OneToOneField(User, on_delete=models.CASCADE)
	name        = models.CharField(max_length=100, null=True, blank=True)
	stars       = models.PositiveIntegerField(null=True, blank=True)
	lat         = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
	lng         = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
	description = models.TextField(default='', null=True, blank=True)

	def __str__(self):
		if self.name:
			return self.name
		else:
			return str(self.user)

@receiver(post_save, sender=User)
def create_hotel(**kwargs):
	if kwargs['created']:
		Hotel.objects.create(user=kwargs['instance'])

class HotelContact(models.Model):

	contact_type_choices = (

		('email', 'Email'),
		('phone', 'Phone')
	)

	hotel        = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	contact_type = models.CharField(max_length=10, choices=contact_type_choices)
	content      = models.CharField(max_length=50)

	def __str__(self):
		return str(hotel) + " - " + str(contact_type)


class HotelPhoto(models.Model):

	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	photo = models.CharField(max_length=100)

	def __str__(self):
		return str(self.hotel)

class HotelRoomType(models.Model):

	room_type_choices = (

		('single', 'Single'),
		('double', 'Double'),
		('trible', 'Trible')
	)

	hotel     = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	room_type = models.CharField(max_length=15, choices=room_type_choices)
	price     = models.DecimalField(max_digits=6, decimal_places=2)

	def __str__(self):
		return str(self.hotel) + " - " + str(self.room_type)

class HotelRoom(models.Model):

	room_type   = models.ForeignKey(HotelRoomType, on_delete=models.CASCADE)
	title       = models.CharField(max_length=100)
	description = models.TextField(default='')
	room_number = models.PositiveIntegerField()

	def __str__(self):
		return str(self.room_type) + " - " + str(self.room_number)

class HotelRoomPhoto(models.Model):

	room  = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
	photo = models.CharField(max_length=100)

	def __str__(self):
		return str(self.room)

class HotelRoomExtension(models.Model):

	room    = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
	content = models.CharField(max_length=100)

	def __str__(self):
		return str(self.room)

class HotelRoomReservation(models.Model):

	fullname     = models.CharField(max_length=50)
	check_in     = models.DateField()
	check_out    = models.DateField()
	total_price  = models.DecimalField(max_digits=6, decimal_places=2)
	phone_number = models.CharField(max_length=20)
	room_number  = models.PositiveIntegerField()
	qr_photo     = models.CharField(max_length=100, null=True, blank=True)

	def __str__(self):
		return self.fullname + " - " + str(self.room_number)