from django import forms
from django.contrib.auth.models import User

from . import models


class BloodForm(forms.ModelForm):
    class Meta:
        model=models.Stock
        fields=['bloodgroup','unit']

class RequestForm(forms.ModelForm):
    class Meta:
        model=models.BloodRequest
        fields=['patient_name','patient_age','reason','bloodgroup','unit']

class UserdistrictForm(forms.ModelForm):
    class Meta:
        model=models.users
        fields=['district','mobile','profile_pic','email']

class UsersdistrictForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password',]
        widgets = {
        'password': forms.PasswordInput()
        }

