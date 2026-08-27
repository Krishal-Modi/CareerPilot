from django import forms
from django.forms import formset_factory
from django.utils import timezone

from .models import JobApplication


class JobApplicationForm(forms.Form):
	company = forms.CharField(max_length=150)
	job_title = forms.CharField(max_length=150, label='Job title')
	job_url = forms.CharField(max_length=500, required=False, label='Application URL')
	location = forms.CharField(max_length=150, required=False)
	work_type = forms.ChoiceField(choices=[('', '---------')] + list(JobApplication.WorkType.choices), required=False)
	job_type = forms.ChoiceField(choices=[('', '---------')] + list(JobApplication.JobType.choices), required=False)
	date_applied = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
	status = forms.ChoiceField(choices=JobApplication.VISIBLE_STATUS_CHOICES)
	source = forms.ChoiceField(choices=JobApplication.Source.choices, required=False)
	follow_up_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
	next_action = forms.CharField(max_length=200, required=False)
	next_action_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
	job_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}), required=False)
	notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)

	def __init__(self, *args, **kwargs):
		instance = kwargs.pop('instance', None)
		super().__init__(*args, **kwargs)
		self.instance = instance
		if instance:
			self.initial.update(instance)
		else:
			self.initial.setdefault('date_applied', timezone.localdate())
		self.initial.setdefault('source', JobApplication.Source.LINKEDIN)

	def clean_status(self):
		status = self.cleaned_data['status']
		return 'applied' if status == 'saved' else status


class ReferralForm(forms.Form):
	referral_id = forms.CharField(required=False, widget=forms.HiddenInput)
	name = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'placeholder': 'Contact name'}))
	email = forms.EmailField(max_length=254, required=False, widget=forms.EmailInput(attrs={'placeholder': 'name@company.com'}))
	contact_number = forms.CharField(max_length=30, required=False)
	contact_type = forms.ChoiceField(choices=(('linkedin', 'LinkedIn'), ('cold_email', 'Cold email')), required=False)


ReferralFormSet = formset_factory(ReferralForm, extra=0, can_delete=True)