from django.urls import path, include
from . import views
from .views import create_prescription

urlpatterns = [
    path('hospital/login/', views.hospital_login_view, name='hospital_login'),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('hospital/home/', views.hospital_home, name='hospital_home'),
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/new/<int:appointment_id>/', create_prescription, name='create_prescription'),
    path("select2/", include("django_select2.urls")),
    # other paths
]
