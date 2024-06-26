# views.py (doctor app)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital
from user.models import Appointment

def hospital_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'hospital'):
            auth_login(request, user)
            return redirect('hospital_dashboard')  # Ensure 'hospital_dashboard' matches your URL name
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'hospital_login.html')

@login_required
def hospital_dashboard(request):
    if hasattr(request.user, 'hospital'):
        hospital = request.user.hospital
        appointments = Appointment.objects.filter(hospital=hospital)
        context = {
            'hospital': hospital,
            'appointments': appointments,
        }
        return render(request, 'hospital_dashboard.html', context)
    else:
        return redirect('hospital_login')  # Redirect back to login if user doesn't have hospital attribute
