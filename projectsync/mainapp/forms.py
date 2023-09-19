from django import forms
from django.contrib.auth.models import User
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    role = forms.CharField(max_length=30)
    class Meta():
        model=User
        fields = ('username','email','password')
