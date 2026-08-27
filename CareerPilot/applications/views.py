import csv

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from google.cloud.firestore_v1.base_query import FieldFilter

from config.firebase import database
from .forms import JobApplicationForm, ReferralFormSet
from .models import JobApplication


def _firestore_application_data(cleaned_data, uid):
    application = dict(cleaned_data)
    application['user_id'] = uid
    for field_name in ('date_applied', 'follow_up_date', 'next_action_date'):
        if application.get(field_name):
            application[field_name] = application[field_name].isoformat()
    return application


def _applications(uid):
    query = database().collection('applications').where(filter=FieldFilter('user_id', '==', uid))
    return [dict(document.to_dict() or {}, pk=document.id) for document in query.stream()]


def _application_sort_key(application):
    date_applied = application.get('date_applied')
    if date_applied is None:
        date_applied = ''
    elif hasattr(date_applied, 'isoformat'):
        date_applied = date_applied.isoformat()
    else:
        date_applied = str(date_applied)
    return date_applied, str(application.get('pk', ''))


def _filtered_applications(request):
    applications = _applications(request.user.uid)
    query = ' '.join(request.GET.get('q', '').split()).lower()
    status = request.GET.get('status', '')
    if query:
        applications = [application for application in applications if query in str(application.get('company', '')).lower() or query in str(application.get('job_title', '')).lower()]
    if status:
        applications = [application for application in applications if application.get('status') == status]
    return applications, query, status


def _save_referrals(application_id, uid, formset):
    collection = database().collection('applications').document(application_id).collection('referrals')
    for form in formset:
        if not form.cleaned_data or not form.cleaned_data.get('name'):
            continue
        referral_id = form.cleaned_data.get('referral_id') or None
        referral = {key: form.cleaned_data.get(key, '') for key in ('name', 'email', 'contact_number', 'contact_type')}
        referral['user_id'] = uid
        if form.cleaned_data.get('DELETE'):
            if referral_id:
                collection.document(referral_id).delete()
            continue
        (collection.document(referral_id) if referral_id else collection.document()).set(referral)


@login_required
def dashboard(request):
    applications, query, status = _filtered_applications(request)
    sort = request.GET.get('sort', 'newest')
    applications.sort(key=_application_sort_key, reverse=sort != 'oldest')
    paginator = Paginator(applications, 8)
    page = paginator.get_page(request.GET.get('page'))
    return render(request, 'dashboard.html', {'applications': page, 'query': query, 'status': status, 'sort': sort, 'status_choices': JobApplication.VISIBLE_STATUS_CHOICES})


@login_required
def application_export(request):
    applications, _, _ = _filtered_applications(request)
    applications.sort(key=_application_sort_key, reverse=True)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="careerpilot-applications.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date of application', 'Company name', 'Company role', 'Location', 'Application URL'])
    for application in applications:
        writer.writerow([application.get('date_applied', ''), application.get('company', ''), application.get('job_title', ''), application.get('location', ''), application.get('job_url', '')])
    return response


@login_required
def application_create(request):
    form = JobApplicationForm(request.POST or None)
    referral_formset = ReferralFormSet(request.POST or None, prefix='referrals')
    if request.method == 'POST' and form.is_valid() and referral_formset.is_valid():
        application = _firestore_application_data(form.cleaned_data, request.user.uid)
        document = database().collection('applications').document()
        document.set(application)
        _save_referrals(document.id, request.user.uid, referral_formset)
        return redirect('dashboard')
    return render(request, 'applications/application_form.html', {'form': form, 'referral_formset': referral_formset, 'page_title': 'Add a job'})


@login_required
def application_update(request, pk):
    document = database().collection('applications').document(pk)
    application = document.get()
    if not application.exists or application.to_dict().get('user_id') != request.user.uid:
        from django.http import Http404
        raise Http404
    data = dict(application.to_dict())
    referrals = [dict(item.to_dict(), referral_id=item.id) for item in document.collection('referrals').stream()]
    form = JobApplicationForm(request.POST or None, initial=data)
    referral_formset = ReferralFormSet(request.POST or None, initial=referrals, prefix='referrals')
    if request.method == 'POST' and form.is_valid() and referral_formset.is_valid():
        updated = _firestore_application_data(form.cleaned_data, request.user.uid)
        document.set(updated)
        _save_referrals(pk, request.user.uid, referral_formset)
        return redirect('dashboard')
    return render(request, 'applications/application_form.html', {'form': form, 'referral_formset': referral_formset, 'page_title': 'Edit application'})


@login_required
def application_status_update(request, pk):
    document = database().collection('applications').document(pk)
    application = document.get()
    if application.exists and application.to_dict().get('user_id') == request.user.uid and request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in {value for value, _ in JobApplication.Status.choices}:
            document.update({'status': new_status})
    return redirect('dashboard')


@login_required
def application_delete(request, pk):
    document = database().collection('applications').document(pk)
    application = document.get()
    if application.exists and application.to_dict().get('user_id') == request.user.uid and request.method == 'POST':
        for referral in document.collection('referrals').stream():
            referral.reference.delete()
        document.delete()
    return redirect('dashboard')
