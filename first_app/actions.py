from .models import Account
from telegram_bot.management.commands import bot
from .auth_tools import AuthTools

def get_buyer_status(buyer):
    if buyer.status < 2:
        return 'Дуже поганий'
    elif buyer.status < 0:
        tatus = 'Поганий'
    elif buyer.status > 0:
        return 'Хороший'
    elif buyer.status > 2:
    	return 'Дуже хороший'

def del_account_as_admin(account, owner):
    account.delete()
    owner.status -= 1
    owner.save()
    if owner.is_banned():
        bot.send_to_buned_user(owner.telegram_id)

def add_product(request):
    name = request.POST["name"]
    game = request.POST["game"] 
    description = request.POST["description"]
    price = request.POST["price"] 
    image = request.FILES["photo"]
    Account.objects.create(image=image, name=name, game=game, description=description, price=price, user=request.user)