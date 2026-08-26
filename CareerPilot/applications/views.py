from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import JobApplicationForm, ReferralFormSet
from .models import JobApplication


@login_required
def dashboard(request):
	applications = JobApplication.objects.filter(user=request.user)
	query = request.GET.get('q', '').strip()
	status = request.GET.get('status', '')
	if query:
		applications = applications.filter(Q(company__icontains=query) | Q(job_title__icontains=query))
	if status:
		applications = applications.filter(status=status)
	paginator = Paginator(applications, 8)
	page = paginator.get_page(request.GET.get('page'))
	return render(request, 'dashboard.html', {'applications': page, 'query': query, 'status': status, 'status_choices': JobApplication.VISIBLE_STATUS_CHOICES})


@login_required
def application_create(request):
	form = JobApplicationForm(request.POST or None)
	referral_formset = ReferralFormSet(request.POST or None)
	if request.method == 'POST' and form.is_valid() and referral_formset.is_valid():
		application = form.save(commit=False)
		application.user = request.user
		application.save()
		referrals = referral_formset.save(commit=False)
		for referral in referrals:
			referral.application = application
			referral.user = request.user
			referral.save()
		return redirect('dashboard')
	return render(request, 'applications/application_form.html', {'form': form, 'referral_formset': referral_formset, 'page_title': 'Add a job'})


@login_required
def application_update(request, pk):
	application = get_object_or_404(JobApplication, pk=pk, user=request.user)
	form = JobApplicationForm(request.POST or None, instance=application)
	referral_formset = ReferralFormSet(request.POST or None, instance=application)
	if request.method == 'POST' and form.is_valid() and referral_formset.is_valid():
		form.save()
		referrals = referral_formset.save(commit=False)
		for referral in referrals:
			referral.user = request.user
			referral.save()
		for referral in referral_formset.deleted_objects:
			referral.delete()
		return redirect('dashboard')
	return render(request, 'applications/application_form.html', {'form': form, 'referral_formset': referral_formset, 'page_title': 'Edit application', 'application': application})


@login_required
def application_status_update(request, pk):
	application = get_object_or_404(JobApplication, pk=pk, user=request.user)
	if request.method == 'POST':
		new_status = request.POST.get('status')
		valid_statuses = {value for value, _ in JobApplication.Status.choices}
		if new_status in valid_statuses or new_status in {'accepted'}:
			application.status = new_status
			application.save(update_fields=('status', 'updated_at'))
	return redirect('dashboard')


@login_required
def application_delete(request, pk):
	application = get_object_or_404(JobApplication, pk=pk, user=request.user)
	if request.method == 'POST':
		application.delete()
	return redirect('dashboard')
