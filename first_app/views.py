from django.shortcuts import render, redirect
import telebot
from django.urls import reverse
from django.contrib.auth.models import User
from . import models
from .auth_tools import AuthTools
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import TelegramUser, Product
from first_app.conf import *
# Create your views here.

bot = telebot.TeleBot(TOKEN1)

def send_buyer(product, owner, buyer):
	bot.send_message(owner.telegram_id, parse_mode='HTML', text=f"Ваш продукт {product.name} хоче придбати цей користувач: <a href='tg://user?id={buyer.telegram_id}'>{buyer.user.username}</a> Якщо ви продали свій обліковий запис, надішліть його ім'я цьому <a href='http://t.me/relend_bot'>боту</a>, або якщо вас ошукали, надішліть /report також цьому <a href='http://t.me/relend_bot'>боту</a>")
	bot.send_message(buyer.telegram_id, parse_mode='HTML', text=f'Ви купили {product.name} у цього користувача: <a href="tg://user?id={owner.telegram_id}">{owner.user.username}</a>? Якщо ви купили обліковий запис, надішліть /buyed цьому <a href="http://t.me/relend_bot">боту</a>, або якщо вас ошукали, надішліть /report також цьому <a href="http://t.me/relend_bot">боту</a>.')


def home_view(request):
	if request.user.is_authenticated:
		return redirect('/home')
	return render(request, 'first_app/home_page.html')

def log_user_home(request):
	user = request.user
	dict_for_page = {'user': user}
	return render(request, 'first_app/loged_user_page.html', context=dict_for_page)
		
def form_view(request):
	if request.user.is_authenticated:
		return redirect('/home')
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
	if request.user.is_authenticated:
		return redirect('/home')
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
		logout(request)
		return redirect('/')
	dict_profile = {'user': user}
	return render(request, 'first_app/profile.html', context=dict_profile)
	
def product_view(request, pr_id):
	product = models.Product.objects.get(pk=pr_id)
	owner = TelegramUser.objects.get(user=product.user)
	buyer = TelegramUser.objects.get(user=request.user)
	dict = {
		'product': product,
		'owner': owner,
		'is_admin': buyer.user.is_staff,
	}
	if 'del' in request.POST:
		product.delete()
		owner.status += -2
		owner.save()
		return redirect('/show')
	elif request.POST:
		send_buyer(product, owner, buyer)
		return render(request, 'first_app/buy.html')
	return render(request, 'first_app/product.html', context=dict)

def del_prod(request, tel_id, name):
	try:
		account = Product.objects.get(name=name)
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

def sold_acount(request, name):
	acount = Product.objects.get(name=name)
	acount.state = 'sold'
	acount.save()
	return HttpResponse('200')

def skam_user(request, username):
	try:
		user = TelegramUser.objects.get(user=User.objects.get(username=username))
	except:
		return HttpResponse('404')
	user.status += -1
	user.save()
	return HttpResponse('200')