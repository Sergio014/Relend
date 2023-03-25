from django.contrib.auth.models import User
from django.http import HttpResponse

from .models import TelegramUser, Account


def del_account(tel_id, name):
	try:
		account = Account.objects.get(name=name)
	except:
		return HttpResponse('400')
	telegram_user = TelegramUser.objects.filter(telegram_id=tel_id)[0]
	if not account.user == telegram_user.user:
		return HttpResponse('400')
	elif not account.state == 'sold':
		return HttpResponse('401')
	account.image.delete()
	account.delete()
	telegram_user.status += 1
	return HttpResponse('200')

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