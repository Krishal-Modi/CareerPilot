from django.contrib.auth import views as auth_views
from django.urls import path

from applications.views import dashboard

from .views import AccountLoginView, dashboard, home, register


urlpatterns = [
    path('', home, name='home'),
    path('applications/', dashboard, name='dashboard'),
    path('accounts/login/', AccountLoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', register, name='register'),
]