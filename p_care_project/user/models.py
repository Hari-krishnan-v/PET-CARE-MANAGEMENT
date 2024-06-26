from django.db import models
from django.contrib.auth.models import User
from doctor.models import Hospital

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
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.treatment_type} on {self.appointment_date}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField()

    def __str__(self):
        return self.user.username

class PetProfile(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        # Add more pet types as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    pet_birthdate = models.DateField()
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)

    def __str__(self):
        return f"{self.pet_name} ({self.pet_type})"
    
class Vaccination(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    next_vaccination_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f"Vaccination for {self.user.username} on {self.next_vaccination_date}"