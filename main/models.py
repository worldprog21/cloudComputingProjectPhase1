from django.contrib.auth.models import PermissionsMixin, Group
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.text import slugify
from main.managers import *
from django.core.mail import send_mail
from django.db import models
from django.core.validators import RegexValidator, validate_slug
from stdimage import StdImageField, JPEGField
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import reverse

class User(AbstractBaseUser, PermissionsMixin):
	phone_regex = RegexValidator(
		regex=r'^\+?1?\d{9,15}$', message="تلفن همراه باید با این فرمت نوشته شود: '+999999999'.")
	phone = models.CharField(
		validators=[phone_regex], max_length=17, unique=True)
	email = models.EmailField(blank=True, null=True)
	first_name = models.CharField(max_length=30, blank=True, null=True)
	last_name = models.CharField(max_length=30, blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = _('User')
		verbose_name_plural = _('Users')
		ordering = ['-last_login']

	def has_group(user, group_name):
		group = Group.objects.get(name=group_name)
		return True if group in user.groups.all() else False

	def email_user(self, subject, message, from_email=None, **kwargs):
		"""
		Sends an email to this User.
		"""
		send_mail(subject, message, from_email, [self.email], **kwargs)

	def __str__(self):
		return self.first_name + ' ' + self.last_name if self.first_name else self.phone


class Media(models.Model):
	name = models.CharField(max_length=254, blank=True, null=True)
	file = StdImageField(upload_to='uploads/%Y/%m/%d/', variations={
		'large': (600, 400),
		'thumbnail': (100, 100, True),
		'medium': (300, 200),
	}, delete_orphans=True)

	def __str__(self):
		if self.name:
			return self.name
		return str(self.file)


class Resturant(models.Model):
	name = models.CharField(max_length=254)
	address = models.TextField(blank=True, null=True)
	is_open = models.BooleanField(default=False)

	def __str__(self):
		return self.name


class ResturantAdmin(models.Model):
	resturant = models.ForeignKey(
		"main.Resturant", on_delete=models.CASCADE, related_name='admins')
	user = models.OneToOneField("main.User", on_delete=models.CASCADE, related_name='admin')

	def __str__(self):
		return ''.join([str(self.user), " : ", str(self.resturant)])


class Category(models.Model):
	name = models.CharField(max_length=254)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=254)
	description = models.TextField(blank=True, null=True)
	category = models.ForeignKey(
		"main.Category", on_delete=models.SET_NULL, null=True, blank=True)
	resturant = models.ForeignKey("main.Resturant", on_delete=models.CASCADE, related_name='products')
	stock = models.IntegerField(default=0)
	price = models.DecimalField(max_digits=9, decimal_places=0, default=0)

	def __str__(self):
		return self.name
	
ORDER_STATUS_CHOICES = (
	(-1, 'Rejected'),
	(0, 'Created'),
	(1, 'Pending'),
	(2, 'Preparation'),
	(3, 'Delivered'),
)
class Order(models.Model):
	user = models.ForeignKey("main.User", on_delete=models.SET_NULL, null=True)
	status = models.IntegerField(choices=ORDER_STATUS_CHOICES, default=0)
	resturant = models.ForeignKey("main.Resturant", on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return ''.join([str(self.user), ' / ', self.get_status_display()])
	

class OrderItem(models.Model):
	order = models.ForeignKey("main.Order", on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey("main.Product", on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=1)

	def __str__(self):
		return ''.join([str(self.product), ': ', str(self.quantity)])
	

	@property
	def total(self):
		return self.quantity * self.product.price