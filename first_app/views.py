from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from . import actions
from .auth_tools import AuthTools
from .models import TelegramUser, Account

from .telegram_bot import send_buyer

def home_view(request):
	if request.user.is_authenticated:
		return redirect('/home')
	return render(request, 'first_app/home_page.html')

def log_user_home(request):
	user = request.user
	dict_for_page = {'user': user}
	return render(request, 'first_app/loged_user_page.html', context=dict_for_page)
		
def register_view(request):
	if request.user.is_authenticated:
		return redirect('/home')
	if request.POST:
		data = request.POST
		username = data.get('username', False)
		password = data.get('password', False)
		username_status = AuthTools.validate_username(username)
		if username_status != 'valid':
			return render(request, 'first_app/register.html', context={f'incorrect_username': 'Username is {username_status}'})
		email = data.get('email', False)
		if AuthTools.get_user_by_email(email) is not None:
			new_eror = {'text': 'This email is already used'}
			return render(request, 'first_app/register.html', context=new_eror)
		user_data = {
			'username': data["username"],
			'first_name': data["fname"],
			'last_name':data["lname"],
			'password': data["password"],
			'email': data["email"]
		}
		AuthTools.register(user_data)
		user = AuthTools.authenticate(username, password)
		AuthTools.login(request, user)
		return redirect('/register_user_in_telegram')
	return render(request, 'first_app/register.html')

def register_telegram_user(request):
	user = request.user
	if request.POST:
		try:
			TelegramUser.objects.get(user=user)
		except:
			return render(request, 'first_app/telegram.html')
		return redirect('/home')
	return render(request, 'first_app/telegram.html')

def login_view(request):
	if request.user.is_authenticated:
		return redirect('/home')
	if request.POST:
		username = request.POST.get('username', False)
		password = request.POST.get('password', False)
		user = AuthTools.authenticate(username, password)
		if user is None:
			incorrect_data_error = {'incorrect_username_or_password': 'Incorect username or password!'}
			return render(request, 'first_app/log_in_page.html', context=incorrect_data_error)
		AuthTools.login(request, user)
		return redirect('/home')
	return render(request, 'first_app/log_in_page.html')

def add_account(request):
	if request.POST:
		actions.add_product(request)
		return redirect('/home')
	return render(request, "first_app/add_account.html")
    
def marketplace_view(request):
	user = request.user
	accounts = Account.objects.all()
	dict = {
				'accounts': accounts,
				'user': user
			}
	return render(request, 'first_app/market.html', context=dict)

def profile_view(request):
	user = request.user
	if 'del_profile' in request.POST:
		user.delete()
		return redirect('/')
	elif request.POST:
		logout(request)
		return redirect('/')
	dict_profile = {'user': user}
	return render(request, 'first_app/profile.html', context=dict_profile)
	
def account_view(request, account_id):
	account = Account.objects.get(pk=account_id)
	owner = TelegramUser.objects.get(user=account.user)
	buyer = TelegramUser.objects.get(user=request.user)
	dict = {
		'account': account,
		'owner': owner,
		'is_owner': owner == buyer,
		'is_admin': buyer.user.is_staff,
	}
	if 'del_as_admin' in request.POST:
		actions.del_account_as_admin(account, owner)
		return redirect('/marketplace')
	
	elif 'del_as_owner' in request.POST:
		account.delete()
		return redirect('/marketplace')
	
	elif request.POST:
		send_buyer(account, owner, buyer, status=actions.get_buyer_status(buyer))
		return render(request, 'first_app/buy.html')
	return render(request, 'first_app/account.html', context=dict)

def contact_us_view(request):
	return render(request, 'first_app/contact_us.html')