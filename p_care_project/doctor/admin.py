from django.contrib import admin
from .models import Hospital
from .models import Medicine, Prescription

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at') 
    list_filter = ('created_at', 'updated_at') 

   
    date_hierarchy = 'created_at'

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'dosage']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'date']