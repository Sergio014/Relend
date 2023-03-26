from django.contrib.auth.models import User
from django.http import HttpResponse
from .auth_tools import AuthTools
from .models import TelegramUser, Account
from telegram_bot.management.commands import bot

def register_telegram_user(username, password, telegram_id):
	user = AuthTools.authenticate(username, password)
	if not user:
		return False
	TelegramUser.objects.create(user=user, telegram_id=telegram_id)
	return True

def confirm_sale(pk, buyer_id, owner_id):
	buyer = TelegramUser.objects.get(pk=buyer_id)
	owner = TelegramUser.objects.get(pk=owner_id)
	try:
		account = Account.objects.get(pk=pk)
	except:
		return "Щось пішло не так :("
	bot.send_notification_to_buyer(account, owner, buyer)
	return '''Я надіслав сповіщення покупцю акаунту.
	Коли він підтвердить покупку, акаунт буде успішно видалено з ринку'''

def del_account(pk):
	try:
		account = Account.objects.get(pk=pk)
	except:
		return "Щось пішло не так :("
	account.image.delete()
	account.delete()
	telegram_user = TelegramUser.objects.get(user=account.user)
	telegram_user.status += 1
	bot.succesfully_sold(telegram_user.telegram_id)
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
		return 'Щось пішло не так :('
	user.status += -1
	user.save()
	return 'Дякую за скаргу'