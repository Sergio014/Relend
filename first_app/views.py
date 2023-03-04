from django.shortcuts import render, redirect
import telebot
from django.urls import reverse
from django.contrib.auth.models import User
from . import models
from .auth_tools import AuthTools
from django.http import HttpResponse
from .models import TelegramUser, Product
from first_app.conf import *
# Create your views here.

bot = telebot.TeleBot(TOKEN1)

def send_buyer(product, owner, buyer):
	bot.send_message(owner.telegram_id, parse_mode='HTML', text=f'Your product {product.name} want to buyed this user: <a href="tg://user?id={buyer.telegram_id}">{buyer.user.username}</a> If you sold your account send its name to this <a href="http://t.me/relend_bot">bot</a>')
	bot.send_message(buyer.telegram_id, parse_mode='HTML', text=f'Did you buyed {product.name} in this user: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a> If you buyed the account send /buyed to this <a href="http://t.me/relend_bot">bot</a>')


def home_view(request):
	return render(request, 'first_app/home_page.html')

def log_user_home(request):
	user = request.user
	dict_for_page = {'user': user}
	return render(request, 'first_app/loged_user_page.html', context=dict_for_page)
		
def form_view(request):
	if request.POST:
		data = request.POST
		username = data.get('username', False)
		password = data.get('password', False)
		try:
			User.objects.get(username=username)
			in_eror = {'text_u': 'Username is already used'}
			return render(request, 'first_app/sign_up.html', context=in_eror)
		except:
			email = data.get('email', False)
		try:
			User.objects.get(email=email)
			new_eror = {'text': 'This email is already used'}
			return render(request, 'first_app/sign_up.html', context=new_eror)
		except:
			user_data = {
			'username': data["username"],
			'first_name': data["fname"],
			'last_name':data["lname"],
			'password': data["password"],
			'email': data["email"]
		}
			AuthTools.register(user_data)
			user =  AuthTools.authenticate(username, password)
			AuthTools.login(request, user)
			return redirect('/t_user')
	else:
		return render(request, 'first_app/sign_up.html')
def register_telegram_user(request):
	user = request.user
	if request.POST:
		try:
			TelegramUser.objects.get(user=user)
			return redirect('/home')
		except:
			return render(request, 'first_app/telegram.html')
	return render(request, 'first_app/telegram.html')
def login_view(request):
	if request.POST:
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		user =  AuthTools.authenticate(username, password)
		if user is None:
			in_error = {'text_u': 'Incorect username or password!'}
			return render(request, 'first_app/log_in_page.html', context=in_error)
		else:
			AuthTools.login(request, user)
			return redirect('/home')
	else:
		return render(request, 'first_app/log_in_page.html')

def add_product(request):
	if request.POST:
		print(request.POST)
		print(request.FILES)
		name = request.POST["name"]
		game = request.POST["game"] 
		description = request.POST["description"]
		price = request.POST["price"] 
		image = request.FILES["photo"]
		Product.objects.create(image=image, name=name, game=game, description=description, price=price, user=request.user)
		return redirect('/home')
	return render(request, "first_app/add_product.html")
    
def marketplace(request):
	user = request.user
	prods = models.Product.objects.all()
	dict = {
				'products': prods,
				'user': user
			}
	return render(request, 'first_app/market.html', context=dict)

def profile_view(request):
	user = request.user
	if request.POST:
		AuthTools.logout(request)
		return redirect('/')
	dict_profile = {'user': user}
	return render(request, 'first_app/profile.html', context=dict_profile)
	
def product_view(request, pr_id):
	product = models.Product.objects.get(pk=pr_id)
	owner = TelegramUser.objects.get(user=product.user)
	buyer = TelegramUser.objects.get(user=request.user)
	dict = {'product': product}
	if request.POST:
		send_buyer(product, owner, buyer)
		return redirect('/show')
	return render(request, 'first_app/product.html', context=dict)

def del_prod(request, tel_id, name):
	try:
		account = Product.objects.get(name=name)
	except:
		return HttpResponse('400')
	# telegram_user = TelegramUser.objects.get(telegram_id=tel_id)
	telegram_user = TelegramUser.objects.filter(telegram_id=tel_id)[1]
	if not account.user == telegram_user.user:
		return HttpResponse('400')
	elif not account.state == 'sold':
		return HttpResponse('401')
	account.delete()
	return HttpResponse('200')

def sold_acount(request, name):
	acount = Product.objects.get(name=name)
	acount.state = 'sold'
	acount.save()
