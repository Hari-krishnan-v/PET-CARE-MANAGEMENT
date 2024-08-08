from django.contrib import admin
from .models import Customer, Appointment ,PetProfile

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('user__date_joined',)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'treatment_type', 'hospital', 'sent_date', 'accepted']
    search_fields = ['name', 'email']
    list_filter = ['treatment_type', 'hospital', 'sent_date', 'accepted']

admin.site.register(Appointment, AppointmentAdmin)

