from django.urls import path
from .views import login_view, form_view, home_view, log_user_home, del_prod, add_product, marketplace, profile_view, product_view, register_telegram_user
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import generics
from .models import TelegramUser
from .serializers import TelegramUserSerializer


app_name = 'first_app'

urlpatterns = [
	path('', home_view, name='home_page'),
	path('home/', log_user_home, name='log_home'),
	path('register/', form_view, name='sign_up_page'),
	path('login/', login_view, name='log_in_page'),
	path('add_product/', add_product, name='add_product_page'),
	path('show/', marketplace, name='show'),
	path('profile/', profile_view, name='profile'),
	path('product/<pr_id>', product_view, name='product'),
	path('t_user/', register_telegram_user, name='register_telegram_user'),
	path('del_prod/<name>', del_prod),
    path('users/', generics.ListCreateAPIView.as_view(queryset=TelegramUser.objects.all(), serializer_class=TelegramUserSerializer), name='user-list')
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
