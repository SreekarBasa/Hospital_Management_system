
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
# created super-user with name-admin
# email address: admin@gmail.com
# password : admin
# Create your views here.

def About(request):
    return render(request, 'about.html')

def Contact(request):
    return render(request, 'contact.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')  # if not logged in redirect here
    return render(request, 'index.html')

def Index(request):
    if not request.user.is_staff:
        return redirect('login')
    doctors = Doctor.objects.all()
    patient = Patient.objects.all()
    appointment = Appointment.objects.all()
    d = 0;
    p = 0;
    a = 0;
    for i in doctors:
        d+=1
    for i in patient:
        p+=1
    for i in appointment:
        a+=1
    x = {'d':d,'p':p,'a':a}
    return render(request, 'index.html', x)
def Login(request):
    error = ""
    if request.method == 'POST':
        usr = request.POST['uname']
        pwd = request.POST['pwd']
        user = authenticate(username=usr, password=pwd)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html', d)

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')

def View_Doctor(request):
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    x = {'doc': doc}
    return render(request, 'view_doctor.html', x)

def Add_Doctor(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        doctor = request.POST['doc_name']
        contact = request.POST['doc_cont']
        specialization = request.POST['doc_spec']
        email = request.POST['doc_email']
        try:
            Doctor.objects.create(name=doctor, mobile=contact, specialization=specialization, email=email)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_doctor.html', d)

def Delete_Doctor(request, pid): # delete on basis of id
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    x = {'pat': pat}
    return render(request, 'view_patient.html', x)

def Add_Patient(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        pat = request.POST['pat_name']
        contact = request.POST['pat_cont']
        gender = request.POST['pat_gen']
        age = request.POST['pat_age']
        addr = request.POST['pat_addr']
        email = request.POST['pat_email']
        try:
            Patient.objects.create(name=pat, mobile=contact, gender=gender, address=addr, email=email, age=age)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'add_patient.html', d)

def Delete_Patient(request, pid): # delete on basis of id
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.get(id=pid)
    pat.delete()
    return redirect('view_patient')

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    apt = Appointment.objects.all()
    x = {'apt': apt}
    return render(request, 'view_appointment.html', x)

def Add_Appointment(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    doc = Doctor.objects.all()
    pat = Patient.objects.all()
    if request.method == 'POST':
        doc_name = request.POST.get('doc_apt')
        pat_name = request.POST.get('pat_apt')
        date = request.POST.get('date_apt')
        time = request.POST.get('time_apt')
        doctor = Doctor.objects.filter(name=doc_name).first()
        patient = Patient.objects.filter(name=pat_name).first()
        try:
            Appointment.objects.create(doctor=doctor, patient=patient, date1=date, time1=time)
            error = "no"
        except Exception as e:
            error = "yes"
            print(f"Error creating appointment: {str(e)}")  # Log the specific error
    x = {'error': error, 'doctor': doc, 'patient': pat}
    return render(request, 'add_appointment.html', x)

def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    apt = Appointment.objects.get(id=pid)
    apt.delete()
    return redirect('view_appointment')



