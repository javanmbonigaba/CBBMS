from django.shortcuts import render,redirect,reverse
from . import forms,models
from .decorators import admin_or_staff_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,response
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from bloodbankmanagement.settings import EMAIL_HOST_USER
from django.contrib.auth.models import User
from donor import models as dmodels
from patient import models as pmodels
from blood import models as umodels
from donor import forms as dforms
from blood import forms
from django.contrib import messages
from patient import forms as pforms
from blood.forms import UserdistrictForm
from blood.models import users

def home_view(request):
    x=models.Stock.objects.all()
    print(x)
    if len(x)==0:
        blood1=models.Stock()
        blood1.bloodgroup="A+"
        blood1.save()

        blood2=models.Stock()
        blood2.bloodgroup="A-"
        blood2.save()

        blood3=models.Stock()
        blood3.bloodgroup="B+"
        blood3.save()        

        blood4=models.Stock()
        blood4.bloodgroup="B-"
        blood4.save()

        blood5=models.Stock()
        blood5.bloodgroup="AB+"
        blood5.save()

        blood6=models.Stock()
        blood6.bloodgroup="AB-"
        blood6.save()

        blood7=models.Stock()
        blood7.bloodgroup="O+"
        blood7.save()

        blood8=models.Stock()
        blood8.bloodgroup="O-"
        blood8.save()

    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')  
    return render(request,'blood/index.html')

def is_donor(user):
    return user.groups.filter(name='DONOR').exists()

def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if request.user.is_superuser:
        return redirect('admin-dashboard')
    elif request.user.is_staff:
        return redirect('user_dashboard_view')
    elif is_donor(request.user):
        return redirect('donor/donor-dashboard')
    elif is_patient(request.user):
        return redirect('patient/patient-dashboard')
    else:
        messages.error(request, 'Your account is not yet associated with a role.')
        return redirect('login')


@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
           
    totalunit=models.Stock.objects.aggregate(Sum('unit'))
    dict={
        'staff_district':staff_district,
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
        'totaldonors':dmodels.Donor.objects.all().count(),
        'totalbloodunit':totalunit['unit__sum'],
        'totalrequest':models.BloodRequest.objects.all().count(),
        'totalapprovedrequest':models.BloodRequest.objects.all().filter(status='Approved').count()
    }
    return render(request,'blood/admin_dashboard.html',context=dict)

@login_required(login_url='adminlogin')
def admin_blood_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    dict={
        'staff_district':staff_district,
        'bloodForm':forms.BloodForm(),
        'A1':models.Stock.objects.get(bloodgroup="A+"),
        'A2':models.Stock.objects.get(bloodgroup="A-"),
        'B1':models.Stock.objects.get(bloodgroup="B+"),
        'B2':models.Stock.objects.get(bloodgroup="B-"),
        'AB1':models.Stock.objects.get(bloodgroup="AB+"),
        'AB2':models.Stock.objects.get(bloodgroup="AB-"),
        'O1':models.Stock.objects.get(bloodgroup="O+"),
        'O2':models.Stock.objects.get(bloodgroup="O-"),
    }
    if request.method=='POST':
        bloodForm=forms.BloodForm(request.POST)
        if bloodForm.is_valid() :        
            bloodgroup=bloodForm.cleaned_data['bloodgroup']
            stock=models.Stock.objects.get(bloodgroup=bloodgroup)
            stock.unit=bloodForm.cleaned_data['unit']
            stock.save()
        return HttpResponseRedirect('admin-blood')
    return render(request,'blood/admin_blood.html',context=dict)


# @login_required(login_url='adminlogin')
# def admin_donor_view(request):
#     donors=dmodels.Donor.objects.all()
#     return render(request,'blood/admin_donor.html',{'donors':donors})
# FIXME:
@login_required(login_url='adminlogin')
def admin_donor_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    if request.user.is_superuser:
        donors=dmodels.Donor.objects.all()
    else:
        staff_district =users.objects.get(user=request.user).district  
        donors = dmodels.Donor.objects.filter(district=staff_district)
    return render(request, 'blood/admin_donor.html', {'donors': donors, 'staff_district':staff_district,})

# def admin_donor_view(request):
#     try:
#         # Retrieve the district of the logged-in user from the blood_users table
#         user_district = blood_users.objects.get(user=request.user).district
#         print(f"Logged-in user's district: {user_district}")

#         # Filter the donors based on the district
#         donors = dmodels.Donor.objects.filter(district=user_district)
#         print(f"Number of donors found: {donors.count()}")

#     except blood_users.DoesNotExist:
#         # Handle the case where the user doesn't exist in the blood_users table
#         donors = dmodels.Donor.objects.none()
#         print("User does not exist in blood_users table.")

#     return render(request, 'blood/admin_donor.html', {'donors': donors})
@login_required(login_url='adminlogin')
def admin_users_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    userdistrict=umodels.users.objects.all()            
    return render(request,'blood/admin_users.html',{'userdistrict':userdistrict, 'staff_district':staff_district,})

@login_required(login_url='adminlogin')
def update_donor_view(request,pk):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    donor=dmodels.Donor.objects.get(id=pk)
    user=dmodels.User.objects.get(id=donor.user_id)
    userForm=dforms.DonorUserForm(instance=user)
    donorForm=dforms.DonorForm(request.FILES,instance=donor)
    mydict={'userForm':userForm,'donorForm':donorForm,'staff_district':staff_district}
    if request.method=='POST':
        userForm=dforms.DonorUserForm(request.POST,instance=user)
        donorForm=dforms.DonorForm(request.POST,request.FILES,instance=donor)
        if userForm.is_valid() and donorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password) 
            # TODO:
            user.save()
            donor=donorForm.save(commit=False)
            donor.user=user
            donor.bloodgroup=donorForm.cleaned_data['bloodgroup']
            donor.save()
            return redirect('admin-donor')
    return render(request,'blood/update_donor.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_donor_view(request,pk):
    donor=dmodels.Donor.objects.get(id=pk)
    user=User.objects.get(id=donor.user_id)
    user.delete()
    donor.delete()
    return HttpResponseRedirect('/admin-donor')

@login_required(login_url='adminlogin')
def admin_patient_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    if request.user.is_superuser:
        patients = pmodels.Patient.objects.all()
    
    else:
        staff_district =users.objects.get(user=request.user).district
        patients = pmodels.Patient.objects.filter(address=staff_district)
    return render(request,'blood/admin_patient.html',{'patients':patients, 'staff_district':staff_district})


@login_required(login_url='adminlogin')
def update_patient_view(request,pk):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    patient=pmodels.Patient.objects.get(id=pk)
    user=pmodels.User.objects.get(id=patient.user_id)
    userForm=pforms.PatientUserForm(instance=user)
    patientForm=pforms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm, 'staff_district':staff_district}
    if request.method=='POST':
        userForm=pforms.PatientUserForm(request.POST,instance=user)
        patientForm=pforms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            return redirect('admin-patient')
    return render(request,'blood/update_patient.html',context=mydict)


@login_required(login_url='adminlogin')
def delete_patient_view(request,pk):
    patient=pmodels.Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return HttpResponseRedirect('/admin-patient')

@login_required(login_url='adminlogin')
def admin_request_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'staff_district':staff_district})

@login_required(login_url='adminlogin')
def admin_request_history_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    requests=models.BloodRequest.objects.all().exclude(status='Pending')
    return render(request,'blood/admin_request_history.html',{'requests':requests,'staff_district':staff_district})

@login_required(login_url='adminlogin')
def admin_donation_view(request):
    if request.user.is_superuser:
        staff_district = "Admin" 
    else:
        staff_district =users.objects.get(user=request.user).district+" "+"District"
    donations=dmodels.BloodDonate.objects.all()
    return render(request,'blood/admin_donation.html',{'donations':donations,'staff_district':staff_district})

@login_required(login_url='adminlogin')
# def update_approve_status_view(request, pk):
#     req = models.BloodRequest.objects.get(id=pk)
#     message = None
#     bloodgroup = req.bloodgroup
#     unit = req.unit
#     stock = models.Stock.objects.get(bloodgroup=bloodgroup)

#     if stock.unit >= unit:
#         stock.unit = stock.unit - unit
#         stock.save()
#         req.status = "Approved"
#         req.save()

#         # Send email notification to the patient
#         patient_email = req.patient.user.email  # Assuming you have a relationship between BloodRequest and PatientFIXME:
#         send_mail(
#             'Blood Request Approved',
#             f'Your request for {unit} units of {bloodgroup} blood has been approved. Please visit the hospital to collect it.',
#             EMAIL_HOST_USER,  # From email
#             [patient_email],  # To email
#             fail_silently=True,
#         )
#     else:
#         message = f"Stock Does Not Have Enough Blood To Approve This Request, Only {stock.unit} Unit Available"

#     requests = models.BloodRequest.objects.all().filter(status='Pending')
#     return render(request, 'blood/admin_request.html', {'requests': requests, 'message': message})

def update_approve_status_view(request,pk):
    
    req=models.BloodRequest.objects.get(id=pk)
    message=None
    bloodgroup=req.bloodgroup
    unit=req.unit
    stock=models.Stock.objects.get(bloodgroup=bloodgroup)
    if stock.unit > unit:
        stock.unit=stock.unit-unit
        stock.save()
        req.status="Approved"
        patient = pmodels.Patient.objects.get(id=req.request_by_patient_id)
        patient_email = patient.user.email
        
        print(f'patient email was {patient_email}')
        send_mail(
            'Blood Request Approved',
            f'Your request for {unit} units of {bloodgroup} blood has been approved. Please visit the hospital to collect it.',
            EMAIL_HOST_USER,  # From email
            [patient_email],  # To email
            fail_silently=True,
        )
        
    else:
        message="Stock Doest Not Have Enough Blood To Approve This Request, Only "+str(stock.unit)+" Unit Available"
    req.save()

    requests=models.BloodRequest.objects.all().filter(status='Pending')
    return render(request,'blood/admin_request.html',{'requests':requests,'message':message})

@login_required(login_url='adminlogin')
def update_reject_status_view(request,pk):
    req=models.BloodRequest.objects.get(id=pk)
    req.status="Rejected"
    req.save()
    return HttpResponseRedirect('/admin-request')

@login_required(login_url='adminlogin')
def approve_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation_blood_group=donation.bloodgroup
    donation_blood_unit=donation.unit

    stock=models.Stock.objects.get(bloodgroup=donation_blood_group)
    stock.unit=stock.unit+donation_blood_unit
    stock.save()
    # donor = dmodels.Donor.objects.get(id=user)
    # patient_email = donor.Email
   
    donor_email = dmodels.Donor.Email
        
    print(f'patient email was {donor_email}')
    send_mail(
        'Blood Request Approved',
        f'Your request for {donation_blood_group} units of {donation_blood_unit} blood has been approved. Thank you!.',
        EMAIL_HOST_USER,  # From email
        [donor_email],  # To email
        fail_silently=True,
    )
    donation.status='Approved'
    donation.save()
    
    return HttpResponseRedirect('/admin-donation')


@login_required(login_url='adminlogin')
def reject_donation_view(request,pk):
    donation=dmodels.BloodDonate.objects.get(id=pk)
    donation.status='Rejected'
    donation.save()
    return HttpResponseRedirect('/admin-donation')


def user_dashboard(request):
    userForm = forms.UsersdistrictForm()
    UserdistrictForm = forms.UserdistrictForm()
    context = {'userForm': userForm, 'UserdistrictForm': UserdistrictForm}
    if request.method == 'POST':
        userForm = forms.UsersdistrictForm(request.POST)
        UserdistrictForm = forms.UserdistrictForm(request.POST, request.FILES)
        if userForm.is_valid() and UserdistrictForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(user.password)  # Hash the password
            is_staff = True
            user.is_staff = True
            user.save()
            users_instance = UserdistrictForm.save(commit=False)
            users_instance.user = user
            users_instance.save()
            my_users, created = Group.objects.get_or_create(name='users')
            my_users.user_set.add(user)
            return redirect('admin_users_view')  # Redirect to appropriate page after successful registration
    return render(request, 'users/users.html', context)