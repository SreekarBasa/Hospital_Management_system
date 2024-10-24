
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.core.mail import send_mail

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

def Update_Doctor(request, pid):
    doc = Doctor.objects.get(id=pid)
    return render(request, 'doc_update.html', {'doc': doc})

def Delete_Doctor(request, pid): # delete on basis of id
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    return redirect('view_doctor')

def Doctor_Notification(request):
    if not request.user.is_staff:
        return redirect('login')
    doctor = Doctor.objects.get(user=request.user)
    pending_appointments = Appointment.objects.filter(doctor=doctor, status='pending')  # gets all pending requests for that doctor
    return render(request, 'doctor_notifications.html', {'appointments': pending_appointments})

# ---------------------- PATIENT -----------------------------#

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

def Update_Patient(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    patient = Patient.objects.get(id=pid)
    if request.methos == 'POST':
        patient.name = request.POST.get('pat')
        patient.contact = request.POST.get('cont')
        patient.gender = request.POST.get('gen')
        patient.age = request.POST.get('age')
        patient.address = request.POST.get('addr')
        patient.email = request.POST.get('email')
        patient.save()
        return render(request, 'view_patient.html', {'patient': patient})
    else:
        return redirect('view_patient')


def Delete_Patient(request, pid): # delete on basis of id
    if not request.user.is_staff:
        return redirect('login')
    pat = Patient.objects.get(id=pid)
    pat.delete()
    return redirect('view_patient')

# ---------------------- APPOINTMENT -----------------------------#

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
    if request.method == 'POST':                # why post.get ??
        doc_name = request.POST.get('doc_apt')  # Retrieves data submitted through a form
        pat_name = request.POST.get('pat_apt')  # It returns none if key doesn't exist in post data
        date = request.POST.get('date_apt')  # if POST['key'] is used it leads to error in none case
        time = request.POST.get('time_apt')  # default value also can be used with post.get
        doctor = Doctor.objects.filter(name=doc_name).first()  # first occurrence
        patient = Patient.objects.filter(name=pat_name).first()
        try:
            appointment = Appointment.objects.create(doctor=doctor, patient=patient, date1=date, time1=time)
            # sending email to doctor
            send_mail(
                'New Appointment Request',
                f'You have a new appointment request from {patient.name} on {date} at {time}. Please accept or reject the appointment.',
                'sreekar.basa2004@gmail.com',  # sender email
                [doctor.email],  # doctor email - recipient
                fail_silently=False,
            )
            error = "no"
        except Exception as e:
            error = "yes"
            print(f"Error creating appointment: {str(e)}")  # Log the specific error
    x = {'error': error, 'doctor': doc, 'patient': pat}
    return render(request, 'add_appointment.html', x)

def Update_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    if request.method == 'POST':
        # Manually update fields from POST data
        appointment.doctor = request.POST.get('doctor')
        appointment.patient = request.POST.get('patient')
        appointment.date1 = request.POST.get('date1')
        appointment.time1 = request.POST.get('time1')
        appointment.save()
        return render(request, 'view_appointment.html', {'appointment': appointment})
    else:
        return redirect('view_appointment')

def Delete_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    apt = Appointment.objects.get(id=pid)
    apt.delete()
    return redirect('view_appointment')

def Accept_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)  # it will be unique
    appointment.status = 'Accepted'  # update the status of appointment
    appointment.save()  # generates a sql update statement that updates the corresponding record in db
    return redirect('view_appointment')

def Reject_Appointment(request, pid):
    if not request.user.is_staff:
        return redirect('login')
    appointment = Appointment.objects.get(id=pid)
    appointment.status = 'Rejected'
    appointment.save()
    return redirect('view_appointment')



