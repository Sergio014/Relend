from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField(default=0)
	telegram_id = models.PositiveBigIntegerField()
	language = models.CharField(max_length=2, default='en')

	def is_banned(self):
		return self.status < -2

class Account(models.Model):
	image = models.FileField(upload_to='images/', null=True, verbose_name="")
	name = models.CharField(max_length=30)
	game = models.CharField(max_length=30)
	description = models.CharField(max_length=255)
	price = models.CharField(max_length=10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)