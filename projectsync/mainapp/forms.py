from django import forms
from .models import User,Tags

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model= User
        fields = ('username','email','password')

class ProjectFilterForm(forms.Form):
    tag = forms.ModelChoiceField(queryset = Tags.objects.all(), empty_label="All tags", required=False)
    search = forms.CharField(max_length=100, required=False)

