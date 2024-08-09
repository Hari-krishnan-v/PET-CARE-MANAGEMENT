from django import forms
from .models import Appointment, TREATMENT_CHOICES
from doctor.models import Hospital
from .models import Vaccination
from .models import PetProfile


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'pet_profile', 'treatment_type', 'hospital', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'pet_profile': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'type': 'tel'}),
        }
    treatment_type = forms.ChoiceField(choices=TREATMENT_CHOICES, label='Treatment Type')
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), label='Hospital')
    pet_profile = forms.ModelChoiceField(queryset=PetProfile.objects.all(), label='Pet Profile')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class VaccinationBookingForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['vaccine_name', 'next_vaccination_date', 'due_date']
        widgets = {
            'vaccine_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'next_vaccination_date': forms.DateInput(attrs={'readonly': 'readonly'}),
            'due_date': forms.DateInput(attrs={'readonly': 'readonly'}),
        }
