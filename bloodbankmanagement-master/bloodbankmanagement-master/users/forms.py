from django import forms
from django.contrib.auth.models import User
from . import models



class UserdistrictForm(forms.ModelForm):
    class Meta:
        model=models.User
        fields=['district','mobile','profile_pic','Email']

class UsersdistrictForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password',]
        widgets = {
        'password': forms.PasswordInput()
        }