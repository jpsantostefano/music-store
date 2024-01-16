from django.contrib.auth.models import User
from django import forms
from .models import Profile, Careers

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','email', 'image']

class CareersForm(forms.ModelForm):
    class Meta:
        model = Careers
        fields = ['full_name', 'email', 'position', 'message', 'cv']