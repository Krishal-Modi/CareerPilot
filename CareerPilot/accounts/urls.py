from django.urls import path

from applications.views import dashboard as applications_dashboard

from .views import AccountLoginView, home, logout, register


urlpatterns = [
    path('', home, name='home'),
    path('applications/', applications_dashboard, name='dashboard'),
    path('accounts/login/', AccountLoginView.as_view(), name='login'),
    path('accounts/logout/', logout, name='logout'),
    path('accounts/register/', register, name='register'),
]