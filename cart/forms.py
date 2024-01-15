from django.contrib.auth.models import User
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'comment-textarea'}),
        }

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)