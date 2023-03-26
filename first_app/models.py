from django.db import models
from django.contrib.auth.models import User

class TelegramUser(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.IntegerField(default=0)
	telegram_id = models.PositiveBigIntegerField()

	def is_banned(self):
		if self.status < -3:
			return True
		return False

class Account(models.Model):
	image = models.FileField(upload_to='images/', null=True, verbose_name="")
	name = models.CharField(max_length=30)
	game = models.CharField(max_length=30)
	description = models.CharField(max_length=255)
	price = models.CharField(max_length=10)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	state = models.CharField(max_length=5, null=True, blank=True)
