from django.contrib.auth.models import User
from django.http import HttpResponse
from .auth_tools import AuthTools
from .models import TelegramUser, Account
from telegram_bot.management.commands import bot
from django.core.exceptions import ObjectDoesNotExist

def register_telegram_user(username, password, telegram_id, lan):
	user = AuthTools.authenticate(username, password)
	if not user:
		return False
	try:
		TelegramUser.objects.get(telegram_id=telegram_id)
	except ObjectDoesNotExist:
		TelegramUser.objects.create(user=user, telegram_id=telegram_id, language=lan)
		return True
	return False

def confirm_sale(pk, buyer_id, owner_id):
	buyer = TelegramUser.objects.get(pk=buyer_id)
	owner = TelegramUser.objects.get(pk=owner_id)
	lan = owner.language
	try:
		account = Account.objects.get(pk=pk)
	except:
		return "Error :("
	bot.send_notification_to_buyer(account, owner, buyer)
	if lan == 'ua':
		return 'Я надіслав сповіщення покупцю акаунту. Коли він підтвердить покупку, акаунт буде успішно видалено з ринку'
	elif lan == 'ru':
		return 'Я послал уведомление покупателю аккаунта. Когда он подтвердит покупку, аккаунт будет успешно удален с рынка'
	else:
		return 'I have sent a notification to the account buyer. When he confirms the purchase, the account will be successfully removed from the market'

def del_account(pk):
	try:
		account = Account.objects.get(pk=pk)
	except:
		return "Error :("
	account.image.delete()
	account.delete()
	telegram_user = TelegramUser.objects.get(user=account.user)
	telegram_user.status += 1
	lan = telegram_user.language
	bot.succesfully_sold(telegram_user.telegram_id, lan)
	if lan == 'ua':
		return 'Успішно куплено'
	elif lan == 'ru':
		return 'Успешно куплено'
	else:
		return 'Purchased successfully'

def report_user(username, language):
	try:
		user = TelegramUser.objects.get(user=User.objects.get(username=username))
	except:
		return 'Error :('
	user.status += -1
	user.save()
	if user.is_banned():
		bot.send_to_buned_user(user.telegram_id, user.language)
	if language == 'ua':
		return 'Дякую за скаргу'
	elif language == 'ru':
		return 'Спасибо за жалобу'
	else:
		return 'Thank you for your report'