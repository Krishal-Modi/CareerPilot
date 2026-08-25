from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class AuthenticationFlowTests(TestCase):
	def test_sessions_persist_for_two_weeks(self):
		self.assertEqual(settings.SESSION_COOKIE_AGE, 60 * 60 * 24 * 14)
		self.assertFalse(settings.SESSION_EXPIRE_AT_BROWSER_CLOSE)

	def test_home_page_is_public(self):
		response = self.client.get(reverse('home'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Turn job hunting into a plan.')
		self.assertContains(response, reverse('login'))
		self.assertContains(response, reverse('register'))

	def test_dashboard_requires_authentication(self):
		response = self.client.get(reverse('dashboard'))

		self.assertRedirects(response, f'{reverse("login")}?next={reverse("dashboard")}')

	def test_user_can_register_and_access_dashboard(self):
		response = self.client.post(
			reverse('register'),
			{
				'email': 'Candidate@Example.com',
				'password1': 'a-strong-test-password-123',
				'password2': 'a-strong-test-password-123',
			},
		)

		self.assertRedirects(response, reverse('login'))
		user = get_user_model().objects.get(username='candidate@example.com')
		self.assertEqual(user.email, 'candidate@example.com')
		response = self.client.post(
			reverse('login'),
			{
				'username': 'CANDIDATE@example.com',
				'password': 'a-strong-test-password-123',
			},
		)

		self.assertRedirects(response, reverse('dashboard'))
		self.assertContains(self.client.get(reverse('dashboard')), 'No applications yet')
from django.test import TestCase

# Create your tests here.
