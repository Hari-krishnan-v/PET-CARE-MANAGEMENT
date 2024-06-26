from django import forms 
from django.contrib.auth.models import User
from django import forms
from .models import Appointment, HOSPITAL_CHOICES, TREATMENT_CHOICES
from doctor.models import Hospital

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'treatment_type', 'hospital', 'appointment_date', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    treatment_type = forms.ChoiceField(choices=TREATMENT_CHOICES, label='Treatment Type', widget=forms.Select(attrs={'class': 'form-control'}))
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), label='Hospital', widget=forms.Select(attrs={'class': 'form-control'}))



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
