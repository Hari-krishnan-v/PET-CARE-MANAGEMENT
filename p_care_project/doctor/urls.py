from django.urls import path
from . import views

urlpatterns = [
    path('hospital/login/', views.hospital_login_view, name='hospital_login'),
    path('hospital/dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    # other paths
]
