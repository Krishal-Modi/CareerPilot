from django.conf import settings
from django.db import models


class Referral(models.Model):
	class ContactType(models.TextChoices):
		LINKEDIN = 'linkedin', 'LinkedIn'
		COLD_EMAIL = 'cold_email', 'Cold email'

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='referrals')
	application = models.ForeignKey('applications.JobApplication', on_delete=models.CASCADE, related_name='referrals')
	name = models.CharField(max_length=150)
	email = models.EmailField(max_length=254, blank=True)
	contact_type = models.CharField(max_length=20, choices=ContactType.choices, default=ContactType.LINKEDIN)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['created_at']
		indexes = [models.Index(fields=['user', 'application'])]

	def __str__(self):
		return f'{self.name} ({self.get_contact_type_display()})'
