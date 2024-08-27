from django import forms
from .models import Appointment, TREATMENT_CHOICES
from doctor.models import Hospital
from .models import Vaccination
from .models import PetProfile

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'email', 'phone', 'treatment_type', 'hospital', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'treatment_type': forms.Select(attrs={'class': 'form-control'}),
            'hospital': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
    treatment_type = forms.ChoiceField(choices=TREATMENT_CHOICES, label='Treatment Type')
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), label='Hospital')
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class VaccinationBookingForm(forms.ModelForm):
    hospital = forms.ModelChoiceField(queryset=Hospital.objects.all(), required=True)
    
    class Meta:
        model = Vaccination
        fields = ['vaccine_name', 'next_vaccination_date', 'due_date', 'hospital']