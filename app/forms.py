from django import forms
from .models import Document
from django.contrib.auth.forms import AuthenticationForm

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)        
