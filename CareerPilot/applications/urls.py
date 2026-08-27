from django.urls import path

from .views import application_create, application_delete, application_export, application_status_update, application_update


urlpatterns = [
	path('applications/add/', application_create, name='application_create'),
	path('applications/export/', application_export, name='application_export'),
	path('applications/<str:pk>/edit/', application_update, name='application_update'),
	path('applications/<str:pk>/status/', application_status_update, name='application_status_update'),
	path('applications/<str:pk>/delete/', application_delete, name='application_delete'),
]