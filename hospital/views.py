
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render

# created super-user with name-admin
# email address: admin@gmail.com
# password : admin
# Create your views here.

# ---------------------- ADMIN/GENERAL -----------------------------#

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
    d = 0
    p = 0
    a = 0
    for i in doctors:
        d += 1
    for i in patient:
        p += 1
    for i in appointment:
        a += 1
    x = {'d': d, 'p': p, 'a': a}
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

# ---------------------- DOCTOR -----------------------------#

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

def Update_Doctor(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.mobile = request.POST.get('mobile')
        doctor.specialization = request.POST.get('spec')
        doctor.email = request.POST.get('email')
        doctor.save()
        return redirect('view_doctor')  # refresh page -- but anyhow content gets updated
    else:
        return redirect('view_doctor')

# def Doctor_Notification(request):
#     if not request.user.is_staff:
#         return redirect('login')
#     doctor = Doctor.objects.get(user=request.user)
#     pending_appointments = Appointment.objects.filter(doctor=doctor, status='pending')  # gets all pending requests for that doctor
#     return render(request, 'doctor_notifications.html', {'appointments': pending_appointments})

# ---------------------- PATIENT -----------------------------#

def View_Patient(request):
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.all()
    x = {'pat': pat}  # dictionary
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

def Update_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.contact = request.POST.get('mobile')
        patient.gender = request.POST.get('gender')
        patient.age = request.POST.get('age')
        patient.address = request.POST.get('address')
        patient.email = request.POST.get('email')
        patient.save()
        # return render(request, 'view_patient.html', {'patient': patient}) -- render with new content
        return redirect('view_patient')  # refresh page -- but anyhow content gets updated
    else:
        return redirect('view_patient')

# ---------------------- APPOINTMENT -----------------------------#

def View_Appointment(request):
    if not request.user.is_staff:
        return redirect('login')
    apt = Appointment.objects.all()
    x = {'apt': apt}
    return render(request, 'view_appointment.html', x)

def send_appointment_email(doctor, patient, date, time):
    email_subject = 'New Appointment Request'
    email_body = f'You have a new appointment request from {patient.name} on {date} at {time}. Please accept or reject the appointment.'
    sender_email = 'information2leak@gmail.com'
    try:
        send_mail(
            email_subject,
            email_body,
            sender_email,
            [doctor.email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {str(e)}")


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

        if doctor is None or patient is None:
            error = "yes"
        else:
            try:
                appointment = Appointment.objects.create(
                    doctor=doctor, patient=patient, date1=date, time1=time
                )

                # Generating accept and reject URLs
                accept_url = request.build_absolute_uri(
                    reverse('accept_appointment', args=[urlsafe_base64_encode(force_bytes(appointment.id))])
                )
                reject_url = request.build_absolute_uri(
                    reverse('reject_appointment', args=[urlsafe_base64_encode(force_bytes(appointment.id))])
                )

                # Email content
                email_subject = 'New Appointment Request'
                email_body = f"""
                    You have a new appointment request from {patient.name} on {date} at {time}.
                    Please respond by clicking one of the following:
                    Accept: {accept_url}
                    Reject: {reject_url}
                """
                sender_email = 'your-email@gmail.com'
                send_mail(
                    email_subject,
                    email_body,
                    sender_email,
                    [doctor.email],
                    fail_silently=False,
                )
                error = "no"
            except Exception as e:
                error = "yes"
                print(f"Error creating appointment: {str(e)}")
    x = {'error': error, 'doctor': doc, 'patient': pat}
    return render(request, 'add_appointment.html', x)


def Update_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    if request.method == 'POST':
        # Manually update fields from POST data
        doc_name = request.POST.get('doctor')
        pat_name = request.POST.get('patient')
        doctor = Doctor.objects.filter(name=doc_name).first()
        patient = Patient.objects.filter(name=pat_name).first()

        if doctor is None or patient is None:
            return redirect('view_appointment')
        else:
            appointment.doctor = doctor
            appointment.patient = patient
            appointment.date1 = request.POST.get('date1')
            appointment.time1 = request.POST.get('time1')
            appointment.save()
            return redirect('view_appointment')
    else:
        return render(request, 'view_appointment.html', {'appointment': appointment})

def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    apt = Appointment.objects.get(id=pid)
    apt.delete()
    return redirect('view_appointment')

def Accept_Appointment(request, encoded_id):
    if not request.user.is_staff:
        return redirect('login')
    app_id = urlsafe_base64_decode(encoded_id).decode()
    appointment = get_object_or_404(Appointment, id=app_id)
    appointment.status = 'Accepted'  # update the status of appointment
    appointment.save()  # generates a sql update statement that updates the corresponding record in db
    return HttpResponse('Appointment accepted. Thank you!!')

def Reject_Appointment(request, encoded_id):
    if not request.user.is_staff:
        return redirect('login')
    app_id = urlsafe_base64_decode(encoded_id).decode()
    appointment = get_object_or_404(Appointment, id=app_id)
    appointment.status = 'Rejected'  # update the status of appointment
    appointment.save()  # generates a sql update statement that updates the corresponding record in db
    return HttpResponse('Appointment rejected. Thank you!!')



