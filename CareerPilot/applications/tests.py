from django.test import RequestFactory, SimpleTestCase
from django.utils import timezone
from unittest.mock import patch

from .forms import JobApplicationForm, ReferralForm
from .models import JobApplication
from .views import _application_summary, _csv_value, _firestore_application_data, _filtered_applications


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

    @patch('applications.views._applications')
    def test_empty_search_returns_all_applications(self, applications):
        applications.return_value = [
            {'company': 'Northwind', 'job_title': 'Engineer'},
            {'company': 'Contoso', 'job_title': 'Designer'},
        ]
        request = RequestFactory().get('/applications/', {'q': '   '})
        request.user = type('User', (), {'uid': 'firebase-user'})()

        results, query, status = _filtered_applications(request)

        self.assertEqual(results, applications.return_value)
        self.assertEqual(query, '')
        self.assertEqual(status, '')

    def test_application_summary_counts_key_statuses(self):
        applications = [
            {'status': JobApplication.Status.APPLIED},
            {'status': JobApplication.Status.ASSESSMENT},
            {'status': JobApplication.Status.INTERVIEW},
            {'status': JobApplication.Status.INTERVIEW},
            {'status': JobApplication.Status.REJECTED},
        ]

        self.assertEqual(_application_summary(applications), {
            'total': 5,
            'assessment': 1,
            'interview': 2,
            'rejected': 1,
        })

    def test_csv_date_value_is_readable(self):
        self.assertEqual(_csv_value('2026-08-27'), '2026-08-27')

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
