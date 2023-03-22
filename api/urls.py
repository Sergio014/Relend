from django.urls import path

from . import views


urlpatterns = [
    path('accounts/', views.AccountsList.as_view()),
    path('accounts/create', views.AccountsListCreate.as_view()),
    path('accounts/<int:pk>', views.AccountRetrieveUpdateDestroyAPIView.as_view()),
]
