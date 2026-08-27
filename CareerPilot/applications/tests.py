from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta

from .forms import JobApplicationForm
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
		status_response = self.client.post(reverse('application_status_update', args=[self.application.pk]), {'status': 'accepted'})

		self.assertEqual(edit_response.status_code, 404)
		self.assertEqual(delete_response.status_code, 404)
		self.assertEqual(status_response.status_code, 404)
		self.assertTrue(JobApplication.objects.filter(pk=self.application.pk).exists())

	def test_owner_can_update_status_from_dashboard(self):
		self.client.force_login(self.owner)

		response = self.client.post(
			reverse('application_status_update', args=[self.application.pk]),
			{'status': 'accepted'},
		)

		self.assertRedirects(response, reverse('dashboard'))
		self.application.refresh_from_db()
		self.assertEqual(self.application.status, JobApplication.Status.ACCEPTED)

	def test_application_form_uses_today_and_requested_fields(self):
		form = JobApplicationForm()

		self.assertEqual(form.initial['date_applied'], timezone.localdate())
		self.assertEqual(form.initial['source'], JobApplication.Source.LINKEDIN)
		self.assertEqual(
			set(form.fields),
			{
				'company', 'job_title', 'job_url', 'location', 'work_type', 'job_type',
				'date_applied', 'status', 'source', 'follow_up_date', 'next_action',
				'next_action_date', 'job_description', 'notes',
			},
		)

	def test_application_form_accepts_plain_text_job_url(self):
		form = JobApplicationForm(
			data={
				'company': 'Plain Text Co',
				'job_title': 'QA Engineer',
				'job_url': 'My success',
				'date_applied': timezone.localdate(),
				'status': JobApplication.Status.SAVED,
			}
		)

		self.assertTrue(form.is_valid(), form.errors)

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

	def test_dashboard_sorts_by_application_date(self):
		older = JobApplication.objects.create(
			user=self.owner,
			company='Older Co',
			job_title='Older role',
			date_applied=timezone.localdate() - timedelta(days=2),
		)
		newer = JobApplication.objects.create(
			user=self.owner,
			company='Newer Co',
			job_title='Newer role',
			date_applied=timezone.localdate(),
		)
		self.client.force_login(self.owner)

		newest_response = self.client.get(reverse('dashboard'))
		oldest_response = self.client.get(reverse('dashboard'), {'sort': 'oldest'})

		self.assertEqual(list(newest_response.context['applications'].object_list), [newer, self.application, older])
		self.assertEqual(list(oldest_response.context['applications'].object_list), [older, self.application, newer])

	def test_export_contains_only_requested_columns_and_owned_applications(self):
		JobApplication.objects.create(
			user=self.owner,
			company='Export Co',
			job_title='Product role',
			location='Remote',
			job_url='https://example.com/job',
		)
		JobApplication.objects.create(user=self.other_user, company='Private Co', job_title='Private role')
		self.client.force_login(self.owner)

		response = self.client.get(reverse('application_export'))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Disposition'], 'attachment; filename="careerpilot-applications.csv"')
		self.assertIn('Date of application,Company name,Company role,Location,Application URL', response.content.decode())
		self.assertIn('Export Co,Product role,Remote,https://example.com/job', response.content.decode())
		self.assertNotIn('Private Co', response.content.decode())
