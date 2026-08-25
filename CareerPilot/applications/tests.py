from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import JobApplication
from contacts.models import Referral


class JobApplicationOwnershipTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.owner = user_model.objects.create_user(
			username='owner@example.com',
			email='owner@example.com',
			password='a-strong-test-password-123',
		)
		self.other_user = user_model.objects.create_user(
			username='other@example.com',
			email='other@example.com',
			password='a-strong-test-password-123',
		)
		self.application = JobApplication.objects.create(
			user=self.owner,
			company='Example Co',
			job_title='Backend Engineer',
		)

	def test_create_assigns_authenticated_owner(self):
		self.client.force_login(self.owner)
		response = self.client.post(
			reverse('application_create'),
			{
				'company': 'New Co',
				'job_title': 'Developer',
				'status': 'saved',
				'priority': 'high',
				'referrals-TOTAL_FORMS': '0',
				'referrals-INITIAL_FORMS': '0',
				'referrals-MIN_NUM_FORMS': '0',
				'referrals-MAX_NUM_FORMS': '1000',
			},
		)

		self.assertRedirects(response, reverse('dashboard'))
		self.assertTrue(JobApplication.objects.filter(user=self.owner, company='New Co').exists())

	def test_other_user_cannot_edit_or_delete_application(self):
		self.client.force_login(self.other_user)

		edit_response = self.client.get(reverse('application_update', args=[self.application.pk]))
		delete_response = self.client.post(reverse('application_delete', args=[self.application.pk]))

		self.assertEqual(edit_response.status_code, 404)
		self.assertEqual(delete_response.status_code, 404)
		self.assertTrue(JobApplication.objects.filter(pk=self.application.pk).exists())

	def test_edit_saves_multiple_referrals(self):
		self.client.force_login(self.owner)
		response = self.client.post(
			reverse('application_update', args=[self.application.pk]),
			{
				'company': 'Example Co',
				'job_title': 'Backend Engineer',
				'status': 'interview',
				'priority': 'high',
				'referrals-TOTAL_FORMS': '2',
				'referrals-INITIAL_FORMS': '0',
				'referrals-MIN_NUM_FORMS': '0',
				'referrals-MAX_NUM_FORMS': '1000',
				'referrals-0-name': 'Alex Rivera',
				'referrals-0-email': 'alex@example.com',
				'referrals-0-contact_type': 'linkedin',
				'referrals-1-name': 'Jamie Chen',
				'referrals-1-email': 'jamie@example.com',
				'referrals-1-contact_type': 'cold_email',
			},
		)

		self.assertRedirects(response, reverse('dashboard'))
		self.assertEqual(Referral.objects.filter(application=self.application, user=self.owner).count(), 2)
