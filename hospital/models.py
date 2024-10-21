from django.db import models

# Create your models here.

# doctor appointment and patient

class Doctor(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    specialization = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

    # class Meta:
    #     app_label = 'DOC'

class Patient(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=5)
    age = models.IntegerField()
    mobile = models.IntegerField()
    address = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)  # if we delete doctors in above, it gets deleted here also
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # patient_age = models.IntegerField() not needed as of now, can be checked using patient info
    # patient_gender = models.CharField(max_length=5)
    # patient_mobile = models.IntegerField()
    date1 = models.DateField()
    time1 = models.TimeField()
    status = models.CharField(max_length=10, choices=[('pending', 'pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending')
    notified = models.BooleanField(default=False)  # default case needed here

    def __str__(self):
        return self.doctor.name+"--"+self.patient.name



