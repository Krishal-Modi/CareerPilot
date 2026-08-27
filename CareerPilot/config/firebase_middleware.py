from types import SimpleNamespace

from django.conf import settings


class FirebaseUserMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):
		uid = request.session.get('firebase_uid')
		email = request.session.get('firebase_email', '')
		username = request.session.get('firebase_username', email.split('@')[0])
		request.user = SimpleNamespace(
			uid=uid,
			email=email,
			username=username,
			is_authenticated=bool(uid),
			is_anonymous=not bool(uid),
		)
		return self.get_response(request)