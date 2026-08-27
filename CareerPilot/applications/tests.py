from django.test import SimpleTestCase
from django.utils import timezone

from .forms import JobApplicationForm, ReferralForm
from .models import JobApplication
from .views import _firestore_application_data


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

    def test_referral_form_has_all_contact_types(self):
        self.assertEqual(
            list(ReferralForm.base_fields['contact_type'].choices),
            [
                ('linkedin', 'LinkedIn'),
                ('indeed', 'Indeed'),
                ('twitter', 'Twitter'),
                ('cold_email', 'Cold email'),
                ('other', 'Other'),
            ],
        )

    def test_application_dates_are_serialized_for_firestore(self):
        form = JobApplicationForm(data={
            'company': 'Firestore Co',
            'job_title': 'Backend Engineer',
            'date_applied': '2026-08-27',
            'follow_up_date': '2026-09-03',
            'next_action_date': '',
            'status': JobApplication.Status.APPLIED,
        })

        self.assertTrue(form.is_valid(), form.errors)
        application = _firestore_application_data(form.cleaned_data, 'firebase-user')

        self.assertEqual(application['date_applied'], '2026-08-27')
        self.assertEqual(application['follow_up_date'], '2026-09-03')
        self.assertIsNone(application['next_action_date'])
