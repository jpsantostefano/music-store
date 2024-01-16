from django.contrib.auth.models import User
from django import forms
from .models import Profile, Careers, Subscriber

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','email', 'image']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class CareersForm(forms.ModelForm):
    class Meta:
        model = Careers
        fields = ['full_name', 'email', 'position', 'message', 'cv']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
            'cv': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

        



class NewsletterSubscriptionForm(forms.Form):
    email = forms.EmailField()
    fields = ['email']