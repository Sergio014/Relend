from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	username = models.CharField(max_length=255, null=True, blank=True)
	password = models.CharField(max_length=255, null=True, blank=True)
	telegram_id = models.PositiveBigIntegerField()

class Product(models.Model):
	image = models.FileField(upload_to='images/', null=True, verbose_name="")
	name = models.CharField(max_length=30)
	category = models.CharField(max_length=30)
	info = models.CharField(max_length=255)
	price = models.CharField(max_length=10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)