import json
import os

import requests
from django.conf import settings


def _initialize():
	import firebase_admin
	from firebase_admin import credentials

	if firebase_admin._apps:
		return
	credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON', '').strip()
	if credentials_json:
		firebase_admin.initialize_app(credentials.Certificate(json.loads(credentials_json)))
	else:
		firebase_admin.initialize_app()


def database():
	from firebase_admin import firestore

	_initialize()
	return firestore.client()


def authenticate(email, password, register=False):
	api_key = settings.FIREBASE_WEB_API_KEY
	endpoint = 'accounts:signUp' if register else 'accounts:signInWithPassword'
	response = requests.post(
		f'https://identitytoolkit.googleapis.com/v1/{endpoint}?key={api_key}',
		json={'email': email, 'password': password, 'returnSecureToken': True},
		timeout=10,
	)
	if response.ok:
		return response.json()
	message = response.json().get('error', {}).get('message', 'Firebase authentication failed.')
	raised = {'EMAIL_EXISTS': 'An account with this email already exists.', 'INVALID_LOGIN_CREDENTIALS': 'Invalid email or password.'}
	raise ValueError(raised.get(message, message.replace('_', ' ').capitalize()))


def user_profile(uid, email):
	document = database().collection('users').document(uid)
	if not document.get().exists:
		document.set({'email': email, 'username': email.split('@')[0]})
	return document.get().to_dict()