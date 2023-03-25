from .models import Account

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
    owner.status -= 2
    owner.save()

def add_product(request):
    name = request.POST["name"]
    game = request.POST["game"] 
    description = request.POST["description"]
    price = request.POST["price"] 
    image = request.FILES["photo"]
    Account.objects.create(image=image, name=name, game=game, description=description, price=price, user=request.user)