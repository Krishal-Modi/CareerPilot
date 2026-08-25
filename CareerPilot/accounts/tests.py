from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthenticationFlowTests(TestCase):
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
