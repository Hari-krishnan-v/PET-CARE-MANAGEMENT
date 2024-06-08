from django.db import models
from django.contrib.auth.models import User

TREATMENT_CHOICES = [
    ('grooming', 'Grooming'),
    ('medical', 'Medical'),
    ('vaccination', 'Vaccination'),
    ('surgery', 'Surgery'),
    # Add more treatment types as needed
]

HOSPITAL_CHOICES = [
    ('hospital_a', 'Hospital A'),
    ('hospital_b', 'Hospital B'),
    ('hospital_c', 'Hospital C'),
    # Add more hospitals as needed
]

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_CHOICES)
    hospital = models.CharField(max_length=50, choices=HOSPITAL_CHOICES)
    appointment_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.treatment_type} on {self.appointment_date}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)