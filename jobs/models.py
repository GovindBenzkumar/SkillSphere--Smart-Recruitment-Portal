from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):

    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    skills = models.ManyToManyField(Skill, blank=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='candidate'
    )

    phone = models.CharField(max_length=15, blank=True)

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    full_name = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )


    age = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    location = models.CharField(
        max_length=200,
        blank=True
    )

    college_name = models.CharField(
        max_length=200,
        blank=True
    )

    degree = models.CharField(
        max_length=200,
        blank=True
    )

    graduation_year = models.CharField(
        max_length=20,
        blank=True
    )

    experience_level = models.CharField(
        max_length=50,
        choices=[
            ('Fresher', 'Fresher'),
            ('Experienced', 'Experienced'),
        ],
        default='Fresher'
    )

    github = models.URLField(
        blank=True,
        null=True
    )

    portfolio_website = models.URLField(
    blank=True,
    null=True
)

    bio = models.TextField(blank=True)


    company_name = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    company_location = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    company_website = models.URLField(
    blank=True,
    null=True
)

    designation = models.CharField(
    max_length=200,
    blank=True,
    null=True
)

    company_description = models.TextField(
    blank=True,
    null=True
)
    company_certificate = models.FileField(
    upload_to='company_certificates/',
    blank=True,
    null=True
)
    

 # Verification fields
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved')],
        default='pending'
    )

    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    company_proof = models.FileField(upload_to='company_docs/', blank=True, null=True)

    project_link = models.URLField(blank=True)
    
    def __str__(self):
        return self.user.username


class Job(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20)
    description = models.TextField()
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    skills = models.ManyToManyField(Skill)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):

    STATUS_CHOICES = [
        ('Applied','Applied'),
        ('Under Review','Under Review'),
        ('Shortlisted','Shortlisted'),
        ('Interview Scheduled','Interview Scheduled'),
        ('Selected','Selected'),
        ('Rejected','Rejected'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Applied'
    )

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"



class Feedback(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    subject = models.CharField(max_length=200)

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


# INTERVIEW MODEL 


class Interview(models.Model):

    MODE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    application = models.OneToOneField(
        Application,
        on_delete=models.CASCADE
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    mode = models.CharField(
        max_length=20,
        choices=MODE_CHOICES
    )

    meeting_link = models.URLField(
        blank=True,
        null=True
    )

    instructions = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.application.user.username} - Interview"
    

class Certificate(models.Model):

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name= 'user_certificates'
    )

    certificate_name = models.CharField(
        max_length=200
    )

    issued_by = models.CharField(
        max_length=200
    )

    certificate_file = models.FileField(
        upload_to='certificates/'
    )

    def __str__(self):

        return self.certificate_name
    

class Project(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    github_link = models.URLField(
        blank=True,
        null=True
    )

    def __str__(self):

        return self.title
    

class Notification(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.message



