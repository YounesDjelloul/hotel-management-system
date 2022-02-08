from django.db import models
from accounts.models import Hotel

# Create your models here.

class HotelContact(models.Model):

	contact_type_choices = (

		('email', 'Email'),
		('phone', 'Phone')
	)

	hotel        = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	contact_type = models.CharField(max_length=10, choices=contact_type_choices)
	content      = models.CharField(max_length=50)

	def __str__(self):
		return str(self.hotel) + " - " + str(self.contact_type)


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
	status       = models.BooleanField(default=False)

	def __str__(self):
		return self.fullname + " - " + str(self.room_number)