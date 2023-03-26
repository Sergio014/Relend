from django.urls import path
from . import views
from . import api
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import generics
from .models import TelegramUser
from .serializers import TelegramUserSerializer


app_name = 'first_app'

urlpatterns = [
	path('', views.home_view, name='home_page'),
	path('contact/', views.contact_us_view, name='contact_us'),
	path('home/', views.log_user_home, name='loged_user_home'),
	path('register/', views.register_view, name='register_page'),
	path('login/', views.login_view, name='log_in_page'),
	path('add_account/', views.add_account, name='add_account_page'),
	path('marketplace/', views.marketplace_view, name='marketplace'),
	path('profile/', views.profile_view, name='profile'),
	path('account/<account_id>', views.account_view, name='account'),
	path('register_user_in_telegram/', views.register_telegram_user, name='register_telegram_user'),
    path('users/', generics.ListCreateAPIView.as_view(queryset=TelegramUser.objects.all(), serializer_class=TelegramUserSerializer), name='user-list'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
