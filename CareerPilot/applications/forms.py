from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone

from contacts.models import Referral
from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		if not self.instance.pk:
			self.initial.setdefault('date_applied', timezone.localdate())

	class Meta:
		model = JobApplication
		fields = (
			'company', 'job_title', 'job_url', 'location', 'work_type', 'job_type',
			'date_applied', 'status', 'source', 'follow_up_date', 'next_action',
			'next_action_date', 'job_description', 'notes',
		)
		widgets = {
			'date_applied': forms.DateInput(attrs={'type': 'date'}),
			'follow_up_date': forms.DateInput(attrs={'type': 'date'}),
			'next_action_date': forms.DateInput(attrs={'type': 'date'}),
			'job_description': forms.Textarea(attrs={'rows': 6}),
			'notes': forms.Textarea(attrs={'rows': 4}),
		}


class ReferralForm(forms.ModelForm):
	class Meta:
		model = Referral
		fields = ('name', 'email', 'contact_type')
		widgets = {
			'name': forms.TextInput(attrs={'placeholder': 'Contact name'}),
			'email': forms.EmailInput(attrs={'placeholder': 'name@company.com'}),
		}


ReferralFormSet = inlineformset_factory(
	JobApplication,
	Referral,
	form=ReferralForm,
	extra=0,
	can_delete=True,
)