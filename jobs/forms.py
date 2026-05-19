from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Job,
    Profile,
    Feedback,
    Interview,
    Certificate,
    Project
)


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = '__all__'

        widgets = {

            'job_type': forms.Select(

                choices=[

                    ('Full Time', 'Full Time'),

                    ('Part Time', 'Part Time'),

                ]

            )

        }

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile
        fields = [

    'full_name',
    'phone',
    'skills',
    'resume',
    'github',
    'portfolio_website',
    'bio',
    'company_website',
    'company_description',

]

        widgets = {

            'skills': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 6
            }),

            'github': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'portfolio_website': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }

class SignupForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    full_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    college_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    degree = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    graduation_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    experience_level = forms.ChoiceField(
        required=False,
        choices=[
            ('Fresher', 'Fresher'),
            ('Experienced', 'Experienced'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    github = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    designation = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        recruiter_fields = [

            'company_name',
            'company_location',
            'company_website',
            'designation',
            'company_description'

        ]

        for field in recruiter_fields:

            self.fields[field].required = False

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = ['subject', 'message']

        widgets = {

            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your feedback here'
            }),
        }


class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = [
            'interview_date',
            'interview_time',
            'mode',
            'meeting_link',
            'instructions'
        ]

        widgets = {

            'interview_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'interview_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),

            'mode': forms.Select(attrs={
                'class': 'form-select'
            }),

            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter meeting link'
            }),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Interview instructions'
            }),
        }



class CertificateForm(forms.ModelForm):

    class Meta:

        model = Certificate

        fields = [
            'certificate_name',
            'issued_by',
            'certificate_file'
        ]

        widgets = {

            'certificate_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'issued_by': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'certificate_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    Job,
    Profile,
    Feedback,
    Interview,
    Certificate,
    Project
)


class JobForm(forms.ModelForm):

    class Meta:

        model = Job

        fields = '__all__'

        widgets = {

            'job_type': forms.Select(

                choices=[

                    ('Full Time', 'Full Time'),

                    ('Part Time', 'Part Time'),

                ]

            )

        }

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [

            'skills',

            'resume',

            'github',

            'portfolio_website',

            'bio',

        ]

        widgets = {

            'skills': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 6
            }),

            'github': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'portfolio_website': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }

class SignupForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    role = forms.ChoiceField(
        choices=Profile.ROLE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    full_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    age = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'
        })
    )

    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    college_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    degree = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    graduation_year = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    experience_level = forms.ChoiceField(
        required=False,
        choices=[
            ('Fresher', 'Fresher'),
            ('Experienced', 'Experienced'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    github = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control'
        })
    )

    designation = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )

    company_description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4
        })
    )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        recruiter_fields = [

            'company_name',
            'company_location',
            'company_website',
            'designation',
            'company_description'

        ]

        for field in recruiter_fields:

            self.fields[field].required = False

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

class FeedbackForm(forms.ModelForm):

    class Meta:

        model = Feedback

        fields = ['subject', 'message']

        widgets = {

            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter subject'
            }),

            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your feedback here'
            }),
        }


class InterviewForm(forms.ModelForm):

    class Meta:

        model = Interview

        fields = [
            'interview_date',
            'interview_time',
            'mode',
            'meeting_link',
            'instructions'
        ]

        widgets = {

            'interview_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'interview_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),

            'mode': forms.Select(attrs={
                'class': 'form-select'
            }),

            'meeting_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter meeting link'
            }),

            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Interview instructions'
            }),
        }



class CertificateForm(forms.ModelForm):

    class Meta:

        model = Certificate

        fields = [
            'certificate_name',
            'issued_by',
            'certificate_file'
        ]

        widgets = {

            'certificate_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'issued_by': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'certificate_file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class RecruiterProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [
            'company_name',
            'company_location',
            'company_website',
            'designation',
            'company_description',
            'phone',
            'company_certificate',
        ]

        widgets = {

            'company_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'company_location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'company_website': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'designation': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'company_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }

       