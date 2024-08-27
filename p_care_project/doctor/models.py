from django.contrib.auth.models import User
from django.db import models
from django.apps import apps


class Hospital(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=255, default='general clinic')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.TextField()

    def __str__(self):
        return self.name 

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=255, default='Unknown')
    description = models.TextField(blank=True, null=True)
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE, related_name='medicines', null=True)

    def __str__(self):
        return self.name


class Prescription(models.Model):
    appointment = models.ForeignKey('user.Appointment', on_delete=models.CASCADE) 
    date = models.DateField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, null=True, related_name='prescriptions')
    dosage = models.CharField(max_length=255)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name='prescriptions', default=1)

    def __str__(self):
        return f'Prescription for {self.appointment} by {self.hospital}'

    def appointment_name(self):
        return self.appointment.name
