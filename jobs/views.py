from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

from django.template.loader import get_template

from django.contrib.auth.views import PasswordChangeView

from django.urls import reverse_lazy

from xhtml2pdf import pisa

import io

from .models import (
    Job,
    Application,
    Profile,
    Interview,
    Certificate,
    Notification
)

from .forms import (
    SignupForm,
    ProfileForm,
    FeedbackForm,
    InterviewForm,
    CertificateForm,
    JobForm,
    RecruiterProfileForm
)


# -------------------------
# Signup View
# -------------------------

def signup_view(request):

    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():

            print(form.cleaned_data['full_name'])

            user = form.save()

            user.email = form.cleaned_data['email']

            user.save()

            profile, created = Profile.objects.get_or_create(
                user=user
            )

            profile.role = form.cleaned_data['role']

            profile.phone = form.cleaned_data['phone']

            profile.full_name = form.cleaned_data['full_name']

            profile.age = form.cleaned_data['age']

            profile.location = form.cleaned_data['location']

            profile.college_name = form.cleaned_data['college_name']

            profile.degree = form.cleaned_data['degree']

            profile.graduation_year = form.cleaned_data['graduation_year']

            profile.experience_level = form.cleaned_data['experience_level']

            profile.github = form.cleaned_data['github']

            profile.bio = form.cleaned_data['bio']

            profile.company_name = form.cleaned_data['company_name']

            profile.company_location = form.cleaned_data['company_location']

            profile.company_website = form.cleaned_data['company_website']

            profile.designation = form.cleaned_data['designation']

            profile.company_description = form.cleaned_data['company_description']

            profile.save()

            return redirect('verify_otp')

        else:

            print(form.errors)

    else:

        form = SignupForm()

    return render(
        request,
        'jobs/signup.html',
        {
            'form': form
        }
    )


# -------------------------
# Home Page
# -------------------------

def home(request):

    return render(
        request,
        'jobs/home.html'
    )


# -------------------------
# Skill Matching Function
# -------------------------

def calculate_match(user_skills, job_skills):

    user_set = set(user_skills)

    job_set = set(job_skills)

    matched = user_set.intersection(job_set)

    if len(job_set) == 0:

        return 0

    return round(
        (len(matched) / len(job_set)) * 100
    )


# -------------------------
# Job List View
# -------------------------

def job_list(request):

    profile = None

    if request.user.is_authenticated:

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )
    jobs = Job.objects.all().order_by('-posted_at')

    applied_jobs = []

    job_matches = []

    applications_count = 0

    shortlisted_count = 0

    interview_count = 0

    profile = None

    if request.user.is_authenticated:

        applied_jobs = Application.objects.filter(
            user=request.user
        ).values_list(
            'job_id',
            flat=True
        )

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

        if profile.role == 'recruiter':

            return redirect('recruiter_dashboard')

        user_skills = list(
            profile.skills.all()
        )

        if profile.role == 'candidate' and not user_skills:

            return redirect('edit_profile')

        for job in jobs:

            job_skills = list(
                job.skills.all()
            )

            match = calculate_match(
                user_skills,
                job_skills
            )

            if match >= 30:

                job_matches.append({

                    "job": job,

                    "match": match

                })

        applications_count = Application.objects.filter(
            user=request.user
        ).count()

        shortlisted_count = Application.objects.filter(
            user=request.user,
            status='Shortlisted'
        ).count()

        interview_count = Application.objects.filter(
            user=request.user,
            status='Interview Scheduled'
        ).count()

    else:

        for job in jobs:

            job_matches.append({

                "job": job,

                "match": 0

            })

    return render(
        request,
        'jobs/job_list.html',
        {

            'job_matches': job_matches,

            'applied_jobs': applied_jobs,

            'profile': profile,

            'applications_count': applications_count,

            'shortlisted_count': shortlisted_count,

            'interview_count': interview_count,

        }
    )


# -------------------------
# Apply Job
# -------------------------

@login_required
def apply_job(request, job_id):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'candidate':

        return redirect('job_list')

    job = get_object_or_404(
        Job,
        id=job_id
    )

    if Application.objects.filter(
        user=request.user,
        job=job
    ).exists():

        return redirect('job_list')

    Application.objects.create(
        user=request.user,
        job=job
    )

    Notification.objects.create(user=request.user, message='Application submitted successfully.')

    Notification.objects.create(
    user=job.recruiter,
    message=f'{request.user.username} applied for {job.title}.'
)
    return redirect('job_list')

    
 


# -------------------------
# Post Job
# -------------------------

@login_required
def post_job(request):

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(
                commit=False
            )

            job.recruiter = request.user

            job.save()

            form.save_m2m()

            return redirect(
                'recruiter_dashboard'
            )

    else:

        form = JobForm()

    return render(
        request,
        'jobs/post_job.html',
        {
            'form': form
        }
    )


# -------------------------
# Candidate Profile Page
# -------------------------

@login_required
def candidate_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    applications_count = Application.objects.filter(
        user=request.user
    ).count()

    shortlisted_count = Application.objects.filter(
        user=request.user,
        status='Shortlisted'
    ).count()

    interview_count = Application.objects.filter(
        user=request.user,
        status='Interview Scheduled'
    ).count()

    context = {

        'profile': profile,

        'applications_count': applications_count,

        'shortlisted_count': shortlisted_count,

        'interview_count': interview_count,

    }

    return render(
        request,
        'jobs/profile.html',
        context
    )


# -------------------------
# Edit Candidate Profile
# -------------------------

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    certificates = Certificate.objects.filter(
        profile=profile
    )

    if request.method == 'POST':

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        certificate_form = CertificateForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()

        if certificate_form.is_valid():

            if certificate_form.cleaned_data.get(
                'certificate_name'
            ):

                certificate = certificate_form.save(
                    commit=False
                )

                certificate.profile = profile

                certificate.save()

        return redirect('profile')

    else:

        form = ProfileForm(
            instance=profile
        )

        certificate_form = CertificateForm()

    return render(
        request,
        'jobs/edit_profile.html',
        {
            'form': form,
            'certificate_form': certificate_form,
            'certificates': certificates,
        }
    )
# -------------------------
# My Applications
# -------------------------

@login_required
def my_applications(request):

    applications = Application.objects.filter(
        user=request.user
    ).select_related('job')

    return render(
        request,
        'jobs/my_applications.html',
        {
            'applications': applications
        }
    )


# -------------------------
# Recruiter Dashboard
# -------------------------

@login_required
def recruiter_dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'recruiter':

        return redirect('job_list')

    jobs = Job.objects.filter(
        recruiter=request.user
    )

    job_data = []

    for job in jobs:

        applicant_count = Application.objects.filter(
            job=job
        ).count()

        job_data.append({

            'job': job,

            'applicant_count': applicant_count

        })

    return render(
    request,
    'jobs/recruiter_dashboard.html',
    {
        'profile': profile,
        'job_data': job_data
    }
)


# -------------------------
# View Applicants
# -------------------------

@login_required
def view_applicants(request, job_id):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'recruiter':

        return redirect('job_list')

    job = get_object_or_404(
        Job,
        id=job_id
    )

    applications = Application.objects.filter(
        job=job
    )

    if request.method == "POST":

        application_id = request.POST.get(
            'application_id'
        )

        new_status = request.POST.get(
            'status'
        )

        application = get_object_or_404(
            Application,
            id=application_id
        )

        application.status = new_status

        application.save()

        Notification.objects.create(
    user=application.user,
    message=f'Your application for {job.title} was updated to {new_status}.'
)

        return redirect(
            'view_applicants',
            job_id=job.id
        )

    applicant_data = []

    for application in applications:

        candidate = application.user

        candidate_profile, created = Profile.objects.get_or_create(
            user=candidate
        )

        user_skills = list(
            candidate_profile.skills.all()
        )

        job_skills = list(
            job.skills.all()
        )

        match = calculate_match(
            user_skills,
            job_skills
        )

        certificates = Certificate.objects.filter(
            profile=candidate_profile
        )

        applicant_data.append({

            'candidate': application.user,

            'match': match,

            'application': application,

            'certificates': certificates,

        })

    applicant_data.sort(
        key=lambda x: x['match'],
        reverse=True
    )

    return render(
        request,
        'jobs/view_applicants.html',
        {

            'job': job,

            'applicant_data': applicant_data

        }
    )


# -------------------------
# Send Feedback
# -------------------------

@login_required
def send_feedback(request):

    if request.method == 'POST':

        form = FeedbackForm(request.POST)

        if form.is_valid():

            feedback = form.save(
                commit=False
            )

            feedback.user = request.user

            feedback.save()

            return redirect('job_list')

    else:

        form = FeedbackForm()

    return render(
        request,
        'jobs/send_feedback.html',
        {
            'form': form
        }
    )


# -------------------------
# Schedule Interview
# -------------------------

@login_required
def schedule_interview(request, application_id):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if profile.role != 'recruiter':

        return redirect('job_list')

    application = get_object_or_404(
        Application,
        id=application_id
    )

    if Interview.objects.filter(
        application=application
    ).exists():

        return redirect(
            'view_applicants',
            job_id=application.job.id
        )

    if request.method == 'POST':

        form = InterviewForm(request.POST)

        if form.is_valid():

            interview = form.save(
                commit=False
            )

            interview.application = application

            interview.save()

            application.status = 'Interview Scheduled'

            application.save()

            Notification.objects.create(
    user=application.user,
    message=f'Interview scheduled for {application.job.title}.'
)

            return redirect(
                'view_applicants',
                job_id=application.job.id
            )

    else:

        form = InterviewForm()

    return render(
        request,
        'jobs/schedule_interview.html',
        {
            'form': form
        }
    )


# -------------------------
# Generate Resume
# -------------------------

@login_required
def generate_resume(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    skills = profile.skills.all()

    certificates = Certificate.objects.filter(
        profile=profile
    )

    context = {

        'user': request.user,

        'profile': profile,

        'skills': skills,

        'certificates': certificates,

    }

    template = get_template(
        'jobs/resume_template.html'
    )

    html = template.render(context)

    result = io.BytesIO()

    pdf = pisa.pisaDocument(
        io.BytesIO(html.encode('UTF-8')),
        result
    )

    if not pdf.err:

        response = HttpResponse(
            result.getvalue(),
            content_type='application/pdf'
        )

        response['Content-Disposition'] = (
            'attachment; filename="resume.pdf"'
        )

        return response

    return HttpResponse(
        'Error generating PDF'
    )


def browse_jobs(request):

    jobs = Job.objects.all()

    query = request.GET.get('q')

    if query:

        jobs = jobs.filter(
            title__icontains=query
        ) | Job.objects.filter(
            company__icontains=query
        ) | Job.objects.filter(
            location__icontains=query
        )

    profile = None

    if request.user.is_authenticated:

        profile, created = Profile.objects.get_or_create(
            user=request.user
        )

    return render(
        request,
        'jobs/browse_jobs.html',
        {
            'jobs': jobs,
            'query': query,
            'profile': profile,
        }
    )


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def edit_recruiter_profile(request):

    profile = request.user.profile

    if request.method == 'POST':

        form = RecruiterProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            return redirect(
                'recruiter_dashboard'
            )

    else:

        form = RecruiterProfileForm(
            instance=profile
        )

    return render(
        request,
        'jobs/edit_recruiter_profile.html',
        {
            'form': form
        }
    )

@login_required
def recruiter_profile(request):

    profile = Profile.objects.get(user=request.user)

    return render(
        request,
        'jobs/recruiter_profile.html',
        {
            'profile': profile
        }
    )

def verify_otp(request):

    if request.method == 'POST':

        otp = request.POST.get('otp')

        if otp == '123456':

            return redirect('login')

    return render(
        request,
        'jobs/verify_otp.html'
    )

class CustomPasswordChangeView(
    PasswordChangeView
):

    template_name = 'jobs/change_password.html'

    def get_success_url(self):

        if self.request.user.profile.role == 'recruiter':

            return reverse_lazy(
                'recruiter_dashboard'
            )

        return reverse_lazy(
            'job_list'
        )

@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'jobs/notifications.html',
        {
            'notifications': notifications
        }
    )