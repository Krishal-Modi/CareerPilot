from django.conf import settings
from django.db import models
from django.utils import timezone


class JobApplication(models.Model):
	class Status(models.TextChoices):
		SAVED = 'saved', 'Saved'
		APPLIED = 'applied', 'Applied'
		PENDING = 'pending', 'Pending'
		ASSESSMENT = 'assessment', 'Assessment'
		INTERVIEW = 'interview', 'Interviewed'
		ACCEPTED = 'accepted', 'Accepted'
		OFFER = 'offer', 'Offer'
		REJECTED = 'rejected', 'Rejected'
		WITHDRAWN = 'withdrawn', 'Withdrawn'

	class WorkType(models.TextChoices):
		REMOTE = 'remote', 'Remote'
		HYBRID = 'hybrid', 'Hybrid'
		ONSITE = 'onsite', 'On-site'

	class JobType(models.TextChoices):
		INTERNSHIP = 'internship', 'Internship'
		COOP = 'coop', 'Co-op'
		FULL_TIME = 'full_time', 'Full-time'
		PART_TIME = 'part_time', 'Part-time'
		CONTRACT = 'contract', 'Contract'

	class Source(models.TextChoices):
		LINKEDIN = 'linkedin', 'LinkedIn'
		COMPANY_WEBSITE = 'company_website', 'Company Website'
		INDEED = 'indeed', 'Indeed'
		GLASSDOOR = 'glassdoor', 'Glassdoor'
		REFERRAL = 'referral', 'Referral'
		RECRUITER = 'recruiter', 'Recruiter'
		COLD_EMAIL = 'cold_email', 'Cold Email'
		UNIVERSITY = 'university', 'University Portal'
		OTHER = 'other', 'Other'

	class Priority(models.TextChoices):
		LOW = 'low', 'Low'
		MEDIUM = 'medium', 'Medium'
		HIGH = 'high', 'High'

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_applications')
	company = models.CharField(max_length=150)
	job_title = models.CharField(max_length=150)
	job_url = models.CharField(max_length=500, blank=True)
	location = models.CharField(max_length=150, blank=True)
	work_type = models.CharField(max_length=20, choices=WorkType.choices, blank=True)
	job_type = models.CharField(max_length=20, choices=JobType.choices, blank=True)
	date_applied = models.DateField(default=timezone.localdate, null=True, blank=True)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
	source = models.CharField(max_length=30, choices=Source.choices, blank=True)
	priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
	salary = models.CharField(max_length=100, blank=True)
	follow_up_date = models.DateField(null=True, blank=True)
	next_action = models.CharField(max_length=200, blank=True)
	next_action_date = models.DateField(null=True, blank=True)
	job_description = models.TextField(blank=True)
	resume_used = models.CharField(max_length=150, blank=True)
	cover_letter_used = models.BooleanField(default=False)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['user', 'status']),
			models.Index(fields=['user', 'date_applied']),
			models.Index(fields=['user', 'follow_up_date']),
		]

	def __str__(self):
		return f'{self.job_title} at {self.company}'
