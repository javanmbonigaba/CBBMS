from django.shortcuts import render,redirect,reverse
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as uforms
from blood import models as umodels 
from users import models 
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.contrib import messages
from blood.models import users



def user_dashboard_view(request):
    staff_district =users.objects.get(user=request.user).district
    return render(request,'users/user_dashboard.html',{"staff_district":staff_district})



def user_login(request):
    if request.method == 'POST':
        form = uforms.UsersdistrictForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  # Make sure the form has a field for username
            password = form.cleaned_data['password']    # Make sure the form has a field for password
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('user_dashboard_view')  # Redirect to the user dashboard
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = uforms.UsersdistrictForm()
    
    return render(request, 'users/user_login.html', {'form': form})
