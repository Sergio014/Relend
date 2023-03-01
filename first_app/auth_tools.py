from django.core import signing
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.conf import settings as django_settings
from rest_framework.authtoken.models import Token

from . import settings as auth_settings
import re


class AuthTools:
	password_salt = auth_settings.AUTH_PASSWORD_SALT
	token_age = auth_settings.AUTH_TOKEN_AGE
	@staticmethod
	def issue_user_token(user, salt):
		if user is not None:
			if salt == 'login':
				token, _ = Token.objects.get_or_create(user=user)
			else:
				token = signing.dumps({"pk": user.pk}, salt=salt)
			return token
		return None
	@staticmethod
	def get_user_from_token(token, salt):
		try:
			value = signing.loads(token, salt)
		except signing.BadSignature:
			return None 
		user = User.objects.get(pk=value['pk'])
		if user is not None:
			return user
		return None
	@staticmethod
	def send_registration_email(user):
		html_template = 'email/welcome_email_configuration.html'
		context = {
			 'username': user.username,
			 'email': user.email,		
		}
	@staticmethod
	def authenticate(username, password):
		user = authenticate(username=username, password=password)
		return user
	@staticmethod
	def get_user_by_email(email):
		if email is not None:
			try:
				user = User.objects.filter(email=email)[0]
				return user
			except:
				pass
		return None

	@staticmethod
	def authenticate_email(email, password):
		if email is not None:
			user = AuthTools.get_user_by_email(email)
			if user is not None:
				user = AuthTools.authenticate(user.username, password)
				return user
		else:
			return False
		return None
	@staticmethod
	def login(request, user):
		if user is not None:
			try:
				login(request, user)
				return True
			except Exception as ex:
				template = "An exception of type {0} occured.Arguments: n{1!r}"
				message= template.format(type(ex).__name__, ex.args)
		return False
	@staticmethod
	def logout(request):
		if request:
			try:
				Token.objects.filter(user=request.user).delete()
				logout(request)
				return True
			except Exception as e:
				pass
		return False 
	@staticmethod
	def register(user_data):
		try:
			user_exists = User.objects.get(email=user_data['email'])
			if user_exists is not None:
				return {
					'is_new': False,
					'invalid': 'email',
				}
			username_exists = User.objects.filter(username=user_data['username'])
			if username_exists is not None:
				return {
					'is_new': False,
					'invalid': 'username',
					}
		except:
			User.objects.create_user(**user_data)
			return {
				"is_new": True,
			}
		return None
	
	@staticmethod
	def set_password(user, password, new_password):
		if user.has_usable_password():
			if user.check_password(password) and password != new_password:
				user.set_password(new_password)
				user.save()
				return True
			elif new_password:
				user.set_password(new_password)
				user.save
				return True
		return False
	@staticmethod
	def reset_password(token, new_password):
		user = AuthTools.get_user_from_token(token, AuthTools.password_salt)
		if user is not None:
			user.set_password(new_password)
			user.save()
			return user
		return None
	@staticmethod
	def validate_username(username):
		min_username_length = 3
		status = "valid"
		if len(username) <= min_username_length:
			status = 'invalid'
		elif re.match("^[a-zA-Z0-9_-]+$", username) is None:
			status = 'invalid'
		else:
			user = AuthTools.get_user_by_username(username)
			if user is not None:
				status = 'taken'
		return status
	@staticmethod
	def validate_email(email):
		status = 'valid'
		try:
			user = AuthTools.get_user_by_email(email)
			if user is not None:
				status = 'taken'
		except:
			status = "invalid"
		return status
	@staticmethod
	def password_check(passwd):
		
		SpecialSym =['$', '@', '#', '%']
		
		if len(passwd) <= 8:
			return 'length should be at least 8'
			
		elif len(passwd) > 20:
			return 'length should be not be greater than 20'
			
		elif not any(char.isdigit() for char in passwd):
			return 'Password should have at least one numeral'
			
		elif not any(char.isupper() for char in passwd):
			return 'Password should have at least one uppercase letter'
			
		elif not any(char.islower() for char in passwd):
			return 'Password should have at least one lowercase letter'
			
		elif not any(char in SpecialSym for char in passwd):
			return 'Password should have at least one of the symbols $@#'
		return None
