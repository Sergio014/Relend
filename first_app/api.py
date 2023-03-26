from django.contrib.auth.models import User
from django.http import HttpResponse
from .auth_tools import AuthTools
from .models import TelegramUser, Account


def register_telegram_user(username, password, telegram_id):
	user = AuthTools.authenticate(username, password)
	if user is None:
		return False
	TelegramUser.objects.create(user=user, telegram_id=telegram_id)
	return True

def del_account(tel_id, name):
	try:
		account = Account.objects.get(name=name)
	except:
		return "Невірне ім'я"
	telegram_user = TelegramUser.objects.filter(telegram_id=tel_id)[0]
	if not account.user == telegram_user.user:
		return "Цей обліковий запис не ваш!"
	elif not account.state == 'sold':
		return 'Покупець акаунту ще не підтвердив цю покупку'
	account.image.delete()
	account.delete()
	telegram_user.status += 1
	return 'Успішно продано'

def add_sold_state(tel_id, name):
	acount = Account.objects.get(name=name)
	acount.state = 'sold'
	acount.save()
	telegram_user = TelegramUser.objects.filter(telegram_id=tel_id)[0]
	telegram_user.status += 1
	return HttpResponse('200')

def report_user(username):
	try:
		user = TelegramUser.objects.get(user=User.objects.get(username=username))
	except:
		return HttpResponse('404')
	user.status += -1
	user.save()
	return HttpResponse('200')