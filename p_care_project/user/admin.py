from django.contrib import admin
from .models import Customer
from .models import Appointment

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('user__date_joined',)
    readonly_fields = ('profile_image',)


admin.site.register(Appointment)