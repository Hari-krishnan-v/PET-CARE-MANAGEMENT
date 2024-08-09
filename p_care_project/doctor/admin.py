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


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'patient', 'pet_profile', 'date', 'hospital', 'dosage')
    search_fields = ('appointment__name', 'patient__username', 'pet_profile__pet_name', 'hospital__name')
    list_filter = ('date', 'hospital', 'appointment__hospital')


admin.site.register(Prescription, PrescriptionAdmin)