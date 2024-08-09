# doctor/forms.py

from django import forms
from django.forms import inlineformset_factory
from .models import Prescription, Medicine


class PrescriptionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Prescription
        fields = ['appointment', 'pet_profile', 'date', 'patient']

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'dosage']

class MedicineWithDosageForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Medicine.objects.all(), empty_label="Select a medicine")
    
    class Meta:
        model = Medicine
        fields = ['name', 'dosage']
# Formset for handling multiple medicines
MedicineFormSet = inlineformset_factory(
    Prescription,
    Medicine,
    form=MedicineWithDosageForm, 
    extra=4,
    can_delete=True
)
