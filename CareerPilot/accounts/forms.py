from django import forms
class EmailUserCreationForm(forms.Form):
	email = forms.EmailField(label='Email address', max_length=254)
	username = forms.CharField(label='Username', max_length=150)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super().clean()
		if cleaned_data.get('password1') != cleaned_data.get('password2'):
			raise forms.ValidationError('Passwords do not match.')
		return cleaned_data


class EmailAuthenticationForm(forms.Form):
	email = forms.EmailField(label='Email address', max_length=254)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)