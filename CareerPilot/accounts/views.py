from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import EmailAuthenticationForm, EmailUserCreationForm


class AccountLoginView(LoginView):
	template_name = 'registration/login.html'
	authentication_form = EmailAuthenticationForm


def register(request):
	if request.user.is_authenticated:
		return redirect('dashboard')

	form = EmailUserCreationForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		form.save()
		return redirect('login')
	return render(request, 'registration/register.html', {'form': form})


def home(request):
	return render(request, 'home.html')


@login_required
def dashboard(request):
	return render(request, 'dashboard.html')

