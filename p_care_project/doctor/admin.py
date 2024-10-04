from django.contrib import admin
from .models import Hospital, Medicine, Prescription

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage')

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'date', 'hospital', 'dosage')  # Adjusted to match the model
    search_fields = ('appointment__name', 'hospital__name')
    list_filter = ('date', 'hospital')

admin.site.register(Prescription, PrescriptionAdmin)
