from django.urls import path

from .views import application_create, application_delete, application_status_update, application_update


urlpatterns = [
	path('applications/add/', application_create, name='application_create'),
	path('applications/<int:pk>/edit/', application_update, name='application_update'),
	path('applications/<int:pk>/status/', application_status_update, name='application_status_update'),
	path('applications/<int:pk>/delete/', application_delete, name='application_delete'),
]