from django.test import SimpleTestCase
from django.urls import reverse
from unittest.mock import patch

from config.firebase import FirebaseConfigurationError
from .forms import EmailAuthenticationForm, EmailUserCreationForm


class FirebaseAuthenticationTests(SimpleTestCase):
    def test_authentication_forms_use_email_fields(self):
        self.assertEqual(list(EmailAuthenticationForm.base_fields), ['email', 'password'])
        self.assertEqual(list(EmailUserCreationForm.base_fields), ['email', 'username', 'password1', 'password2'])

    def test_home_page_is_public(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('login'))
        self.assertContains(response, reverse('register'))

    @patch('accounts.views.authenticate')
    def test_registration_shows_firebase_configuration_error(self, authenticate):
        authenticate.side_effect = FirebaseConfigurationError('Firebase is unavailable.')

        response = self.client.post(reverse('register'), {
            'email': 'new@example.com',
            'username': 'newuser',
            'password1': 'A secure password 123!',
            'password2': 'A secure password 123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firebase is unavailable.')

    @patch('accounts.views.user_profile')
    @patch('accounts.views.authenticate')
    def test_login_shows_firestore_configuration_error(self, authenticate, user_profile):
        authenticate.return_value = {'localId': 'firebase-user', 'email': 'new@example.com'}
        user_profile.side_effect = FirebaseConfigurationError('Firebase Firestore is unavailable.')

        response = self.client.post(reverse('login'), {
            'email': 'new@example.com',
            'password': 'A secure password 123!',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Firebase Firestore is unavailable.')
