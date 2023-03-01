from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from . import models
from .forms import addForm
from .auth_tools import AuthTools
from .models import TelegramUser
# Create your views here.

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
    context = {}
    if request.POST:
        form = addForm(request.POST, request.FILES)
        if form.is_valid() == False or True:
            name = form.cleaned_data.get("name")
            category = form.cleaned_data.get("category") 
            info = form.cleaned_data.get("info")
            price = form.cleaned_data.get("price") 
            img = form.cleaned_data.get("image")
            obj = models.Product.objects.create(image=img, name=name, category=category, info=info, price=price, user=request.user)
            obj.save()
            return redirect('/home')
    form = addForm()
    user = request.user
    context = {
	    		'form': form,
				'user': user
		   	}
    return render(request, "first_app/add_product.html", context)
    
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
	products = models.Product.objects.filter(user=user).all()
	dict_profile = {
					'user': user,
					'products': products
				}
	return render(request, 'first_app/profile.html', context=dict_profile)
	
def product_view(request, pr_id):
	product = models.Product.objects.get(pk=pr_id)
	dict = {'product': product}
	return render(request, 'first_app/product.html', context=dict)