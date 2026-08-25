from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm


class EmailUserCreationForm(UserCreationForm):
	email = forms.EmailField(label='Email address', max_length=254)

	class Meta(UserCreationForm.Meta):
		model = get_user_model()
		fields = ('email',)

	def clean_email(self):
		email = self.cleaned_data['email'].strip().lower()
		if get_user_model().objects.filter(username__iexact=email).exists():
			raise forms.ValidationError('An account with this email already exists.')
		return email

	def save(self, commit=True):
		user = super().save(commit=False)
		user.email = self.cleaned_data['email']
		user.username = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class EmailAuthenticationForm(AuthenticationForm):
	username = forms.EmailField(label='Email address', max_length=254)

	def clean_username(self):
		return self.cleaned_data['username'].strip().lower()