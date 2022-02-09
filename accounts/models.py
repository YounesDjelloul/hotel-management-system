from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class UserManager(BaseUserManager):

	def create_user(self, email, password, stripe_account):
		if email and password:
			user = User(email=email, stripe_account=stripe_account)
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

	email          = models.EmailField(unique=True)
	stripe_account = models.CharField(max_length=200, default="")

	USERNAME_FIELD  = 'email'
	REQUIRED_FIELDS = []
	objects         = UserManager()

	def __str__(self):
		return str(self.email)

class Hotel(models.Model):

	user           = models.OneToOneField(User, on_delete=models.CASCADE)
	name           = models.CharField(max_length=100, null=True, blank=True)
	stars          = models.PositiveIntegerField(null=True, blank=True)
	lat            = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
	lng            = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
	city           = models.CharField(max_length=100, default="")
	description    = models.TextField(default='', null=True, blank=True)

	def __str__(self):
		if self.name:
			return self.name
		else:
			return str(self.user)

@receiver(post_save, sender=User)
def create_hotel(**kwargs):
	if kwargs['created']:
		Hotel.objects.create(user=kwargs['instance'])