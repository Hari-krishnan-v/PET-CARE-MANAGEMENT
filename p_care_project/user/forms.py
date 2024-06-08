from django import forms 
from django.contrib.auth.models import User
from django import forms
from .models import Appointment, HOSPITAL_CHOICES, TREATMENT_CHOICES

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'treatment_type', 'hospital', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    treatment_type = forms.ChoiceField(choices=TREATMENT_CHOICES, label='Treatment Type', widget=forms.Select(attrs={'class': 'form-control'}))
    hospital = forms.ChoiceField(choices=HOSPITAL_CHOICES, label='Hospital', widget=forms.Select(attrs={'class': 'form-control'}))


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
