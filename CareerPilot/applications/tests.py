from django.test import SimpleTestCase
from django.utils import timezone

from .forms import JobApplicationForm, ReferralForm
from .models import JobApplication


class FirebaseApplicationFormTests(SimpleTestCase):
    def test_application_form_has_today_and_linkedin_defaults(self):
        form = JobApplicationForm()

        self.assertEqual(form.initial['date_applied'], timezone.localdate())
        self.assertEqual(form.initial['source'], JobApplication.Source.LINKEDIN)

    def test_application_form_accepts_plain_text_job_url(self):
        form = JobApplicationForm(data={
            'company': 'Plain Text Co',
            'job_title': 'QA Engineer',
            'job_url': 'My success',
            'date_applied': timezone.localdate(),
            'status': JobApplication.Status.APPLIED,
        })

        self.assertTrue(form.is_valid(), form.errors)

    def test_referral_form_has_contact_number(self):
        self.assertIn('contact_number', ReferralForm.base_fields)
