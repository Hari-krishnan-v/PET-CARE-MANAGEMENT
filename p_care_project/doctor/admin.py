from django.contrib import admin
from .models import Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')  # Adjust according to your model fields
    list_filter = ('created_at', 'updated_at')  # Adjust according to your model fields

    # Optionally, if created_at and updated_at are DateTimeField or DateField
    date_hierarchy = 'created_at'  # Provides a date-based drilldown navigation in the admin interface
