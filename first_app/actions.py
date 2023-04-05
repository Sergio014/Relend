from .models import Account
from telegram_bot.management.commands import bot
from .auth_tools import AuthTools
from django.utils import timezone

def is_max_amount_of_accounts(user):
	accounts = Account.objects.filter(user=user, created_at__gte=timezone.now() - timezone.timedelta(days=1))
	amount_of_accounts = len(accounts)
	if amount_of_accounts >= 3:
		return True
	else:
		return amount_of_accounts

def get_buyer_status(buyer):
    print(buyer.status)
    if buyer.status < -2:
        return '👎🏼👎🏼'
    elif buyer.status < 0:
        tatus = '👎🏼'
    elif buyer.status == 0:
        return 'Unknown'
    elif buyer.status > 0:
        return '👍🏼'
    elif buyer.status > 2:
    	return '👍🏼👍🏼'

def del_account_as_admin(account, owner):
    account.delete()
    owner.status -= 1
    owner.save()
    if owner.is_banned():
        bot.send_to_buned_user(owner.telegram_id)

def add_product(request):
    if is_max_amount_of_accounts(user=request.user) is True:
        return "You have exceeded your limit for today, please try again in 24 hours."
    name = request.POST["name"]
    game = request.POST["game"] 
    description = request.POST["description"]
    price = request.POST["price"]
    currency  = request.POST["currency"][0]
    image = request.FILES["photo"]
    Account.objects.create(image=image, name=name, game=game, description=description, price=price, currency=currency, user=request.user)
    return None
