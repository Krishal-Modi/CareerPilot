from django.test import SimpleTestCase
from django.urls import reverse

from .forms import EmailAuthenticationForm, EmailUserCreationForm


class FirebaseAuthenticationTests(SimpleTestCase):
    def test_authentication_forms_use_email_fields(self):
        self.assertEqual(list(EmailAuthenticationForm.base_fields), ['email', 'password'])
        self.assertEqual(list(EmailUserCreationForm.base_fields), ['email', 'password1', 'password2'])

    def test_home_page_is_public(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('login'))
        self.assertContains(response, reverse('register'))
