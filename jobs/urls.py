from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path('login/', auth_views.LoginView.as_view(template_name='jobs/login.html'), name='login'),

    path('signup/', views.signup_view, name='signup'),

    path('logout/', views.logout_view, name='logout'),

    path('jobs/', views.job_list, name='job_list'),

    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),

    path('edit-recruiter-profile/', views.edit_recruiter_profile, name='edit_recruiter_profile'),

    path('post-job/', views.post_job, name='post_job'),

    path('profile/', views.candidate_profile, name='profile'),

    path('my-applications/', views.my_applications, name='my_applications'),

    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),

    path('job/<int:job_id>/applicants/', views.view_applicants, name='view_applicants'),

    path('browse-jobs/',views.browse_jobs,name='browse_jobs'),

    path('feedback/', views.send_feedback, name='send_feedback'),

    path('schedule-interview/<int:application_id>/',views.schedule_interview,name='schedule_interview'),

    path('generate-resume/',views.generate_resume,name='generate_resume'),

    path('edit-profile/',views.edit_profile,name='edit_profile'),

    path('recruiter-profile/',views.recruiter_profile,name='recruiter_profile'),

    path('verify-otp/', views.verify_otp, name='verify_otp'),

    path('change-password/',views.CustomPasswordChangeView.as_view(),name='change_password'),

    path('notifications/',views.notifications,name='notifications'),

]