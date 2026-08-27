import json
import os

import requests
from django.conf import settings


class FirebaseConfigurationError(Exception):
	pass


def _initialize():
	import firebase_admin
	from firebase_admin import credentials

	if firebase_admin._apps:
		return
	credentials_json = os.environ.get('FIREBASE_CREDENTIALS_JSON', '').strip()
	if not credentials_json:
		raise FirebaseConfigurationError('Firebase credentials are not configured on the server.')
	try:
		service_account = json.loads(credentials_json)
		firebase_admin.initialize_app(credentials.Certificate(service_account))
	except (ValueError, TypeError, json.JSONDecodeError) as error:
		raise FirebaseConfigurationError('Firebase credentials are invalid on the server.') from error


def database():
	from firebase_admin import firestore

	try:
		_initialize()
		return firestore.client()
	except FirebaseConfigurationError:
		raise
	except Exception as error:
		raise FirebaseConfigurationError('Firebase Firestore is not configured correctly on the server.') from error


def authenticate(email, password, register=False):
	api_key = settings.FIREBASE_WEB_API_KEY
	if not api_key:
		raise FirebaseConfigurationError('Firebase Web API key is not configured on the server.')
	endpoint = 'accounts:signUp' if register else 'accounts:signInWithPassword'
	try:
		response = requests.post(
			f'https://identitytoolkit.googleapis.com/v1/{endpoint}?key={api_key}',
			json={'email': email.strip().lower(), 'password': password, 'returnSecureToken': True},
			timeout=10,
		)
	except requests.RequestException as error:
		raise FirebaseConfigurationError('Firebase authentication is temporarily unavailable.') from error
	if response.ok:
		try:
			payload = response.json()
		except ValueError as error:
			raise FirebaseConfigurationError('Firebase authentication returned an invalid response.') from error
		if not isinstance(payload, dict) or not payload.get('localId'):
			raise FirebaseConfigurationError('Firebase authentication returned an incomplete response.')
		return payload
	try:
		payload = response.json()
	except ValueError as error:
		raise FirebaseConfigurationError('Firebase authentication returned an invalid response.') from error
	message = payload.get('error', {}).get('message', 'Firebase authentication failed.') if isinstance(payload, dict) else 'Firebase authentication failed.'
	raised = {'EMAIL_EXISTS': 'An account with this email already exists.', 'INVALID_LOGIN_CREDENTIALS': 'Invalid email or password.'}
	raise ValueError(raised.get(message, message.replace('_', ' ').capitalize()))


def user_profile(uid, email):
	document = database().collection('users').document(uid)
	profile = document.get()
	if not profile.exists:
		document.set({'email': email, 'username': email.split('@')[0]})
		return {'email': email, 'username': email.split('@')[0]}
	return profile.to_dict()