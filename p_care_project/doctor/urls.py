from django.urls import path, include
from . import views
from .views import create_prescription

urlpatterns = [
    path('hospital/login/', views.hospital_login_view, name='hospital_login'),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/home/', views.hospital_home, name='hospital_home'),
    path('todays_appointments/', views.todays_appointments, name='todays_appointments'),
    path('prescriptions/new/<int:appointment_id>/', create_prescription, name='create_prescription'),
    path('vaccine-bookings/', views.vaccine_bookings, name='vaccine_bookings'), 
    path("select2/", include("django_select2.urls")),
    path('hospital/profile', views.doctor_profile, name='doctor_profile'),
    # other paths
]
