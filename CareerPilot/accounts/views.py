from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from config.firebase import FirebaseConfigurationError, authenticate, user_profile
from .forms import EmailAuthenticationForm, EmailUserCreationForm


class AccountLoginView(LoginView):
	template_name = 'registration/login.html'
	redirect_authenticated_user = True

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.pop('request', None)
		return kwargs

	def get_form_class(self):
		return EmailAuthenticationForm

	def form_valid(self, form):
		try:
			firebase_user = authenticate(form.cleaned_data['email'], form.cleaned_data['password'])
		except (ValueError, FirebaseConfigurationError) as error:
			form.add_error(None, str(error))
			return self.form_invalid(form)
		try:
			profile = user_profile(firebase_user['localId'], firebase_user['email'])
		except FirebaseConfigurationError as error:
			form.add_error(None, str(error))
			return self.form_invalid(form)
		self.request.session['firebase_uid'] = firebase_user['localId']
		self.request.session['firebase_email'] = firebase_user['email']
		self.request.session['firebase_username'] = profile.get('username', firebase_user['email'].split('@')[0])
		return redirect(self.get_success_url())


def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	form = EmailUserCreationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		try:
			firebase_user = authenticate(form.cleaned_data['email'], form.cleaned_data['password1'], register=True)
		except (ValueError, FirebaseConfigurationError) as error:
			form.add_error(None, str(error))
		else:
			try:
				user_profile(firebase_user['localId'], firebase_user['email'], form.cleaned_data['username'])
			except FirebaseConfigurationError as error:
				form.add_error(None, str(error))
			else:
				return redirect('login')
	return render(request, 'registration/register.html', {'form': form})


def home(request):
	return render(request, 'home.html')


def logout(request):
	request.session.flush()
	return redirect('login')


@login_required
def dashboard(request):
	return render(request, 'dashboard.html')

