# views.py (doctor app)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital
from user.models import Appointment
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Prescription, Medicine
from .forms import PrescriptionForm, MedicineWithDosageForm ,MedicineFormSet
from user.models import Notification

def hospital_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and hasattr(user, 'hospital'):
            auth_login(request, user)
            return redirect('hospital_home')  # Ensure 'hospital_dashboard' matches your URL name
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'hospital_login.html')


@login_required
def hospital_dashboard(request):
    if hasattr(request.user, 'hospital'):
        hospital = request.user.hospital
        appointments_list = Appointment.objects.filter(hospital=hospital).order_by('-sent_date')
        paginator = Paginator(appointments_list, 3)
        page = request.GET.get('page')

        try:
            appointments = paginator.page(page)
        except PageNotAnInteger:
            appointments = paginator.page(1)
        except EmptyPage:
            appointments = paginator.page(paginator.num_pages)
        
        if request.method == 'POST':
            if 'accept_appointment' in request.POST:
                appointment_id = request.POST.get("appointment-id")
                appointment = Appointment.objects.get(id=appointment_id)
                appointment.scheduled_date = request.POST.get("date")
                appointment.accepted = True
                appointment.accepted_date = datetime.datetime.now()
                appointment.save()
                messages.success(request, 'Appointment accepted successfully.')

                # Create a notification for the user
                message = f"Your appointment scheduled on {appointment.scheduled_date} has been accepted."
                Notification.objects.create(user=appointment.user, message=message)

            elif 'clear_appointments' in request.POST:
                Appointment.objects.filter(hospital=hospital).delete()
                messages.success(request, 'All appointments cleared successfully.')

        context = {
            'hospital': hospital,
            'appointments': appointments,
        }
        return render(request, 'hospital_dashboard.html', context)
    else:
        return redirect('hospital_login')


@login_required
def create_prescription(request):
    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        formset = MedicineFormSet(request.POST, prefix='medicines')

        if prescription_form.is_valid() and formset.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.hospital = request.user.hospital
            prescription.save()
            
            medicines = formset.save(commit=False)
            for medicine in medicines:
                medicine.prescription = prescription
                medicine.save()
            
            messages.success(request, 'Prescription created successfully!')
            # Redirect to the prescription list or another page
    else:
        prescription_form = PrescriptionForm()
        formset = MedicineFormSet(prefix='medicines')

    return render(request, 'create_prescription.html', {
        'prescription_form': prescription_form,
        'formset': formset,
    })


@login_required
def prescription_list(request):
    prescriptions = Prescription.objects.filter(hospital=request.user.hospital)
    return render(request, 'prescription_list.html', {'prescriptions': prescriptions})

def hospital_home(request):
    return render(request, 'home_doc.html')