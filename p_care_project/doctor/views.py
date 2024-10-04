# views.py (doctor app)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital
from user.models import Appointment
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Prescription, Medicine
from .forms import PrescriptionForm, MedicineWithDosageForm ,MedicineFormSet
from user.models import Notification,Vaccination
from django.utils import timezone

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
                
                # Parse the scheduled date and time
                scheduled_date = request.POST.get("date", "").strip()
                scheduled_time = request.POST.get("time", "").strip()
                
                if scheduled_date and scheduled_time:
                    scheduled_datetime_str = f"{scheduled_date} {scheduled_time}"
                    
                    try:
                        # Combine and parse date and time
                        scheduled_datetime = datetime.strptime(scheduled_datetime_str, "%Y-%m-%d %H:%M")
                        appointment.scheduled_date = timezone.make_aware(scheduled_datetime)
                        appointment.accepted = True
                        appointment.accepted_date = timezone.now()
                        appointment.save()
                        
                        messages.success(request, 'Appointment accepted successfully.')

                        # Create a notification for the user
                        message = f"Your appointment scheduled on {appointment.scheduled_date.strftime('%Y-%m-%d at %H:%M')} has been accepted."
                        Notification.objects.create(user=appointment.user, message=message)
                    except ValueError:
                        messages.error(request, 'Invalid date or time format.')
                else:
                    messages.error(request, 'Date and time cannot be empty.')

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
def todays_appointments(request):
    today = timezone.now().date()  # Get today's date
    hospital = request.user.hospital

    print(f"Today's Date: {today}")
    print(f"Hospital: {hospital}")

    # Filter appointments to show only accepted ones scheduled for today
    appointments = Appointment.objects.filter(
        hospital=hospital,
        accepted=True,
        scheduled_date__date=today
    ).order_by('-scheduled_date')
    print(f"{appointments}")
    context = {
        'appointments': appointments
    }
    
    return render(request, 'todays_appointments.html', context)

@login_required
def create_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    pet_profile = appointment.pet_profile
    doctor = request.user.hospital

    if request.method == 'POST':
        prescription_form = PrescriptionForm(request.POST)
        formset = MedicineFormSet(request.POST, prefix='medicines')

        if prescription_form.is_valid() and formset.is_valid():
            prescription = prescription_form.save(commit=False)
            prescription.patient = appointment.user  # Link the prescription to the user connected to the appointment
            prescription.appointment = appointment
            prescription.hospital = appointment.hospital  # Automatically set the hospital
            prescription.date = timezone.now().date()  # Automatically set the current date
            prescription.save()
            medicines = formset.save(commit=False)
            for medicine in medicines:
                medicine.prescription = prescription
                print(medicine.prescription)
                medicine.save()
            
            messages.success(request, 'Prescription created successfully!')
         # Adjust redirect as needed

    else:
        # Initialize the form with default values
        initial_data = {
            'appointment': appointment,
            'pet_profile': pet_profile,
            'date': timezone.now().date(),
            'hospital': doctor
        }
        prescription_form = PrescriptionForm(initial=initial_data)
        formset = MedicineFormSet(prefix='medicines')

    return render(request, 'create_prescription.html', {
        'prescription_form': prescription_form,
        'formset': formset,
        'appointment': appointment,
        'pet_profile': pet_profile,
    })



def hospital_home(request):
    appointment_count = Appointment.objects.filter(hospital=request.user.hospital).count()

    appointment = Appointment.objects.first()  
    context = {
        'appointment_count': appointment_count,
        'appointment_id': appointment.id if appointment else '',  # Make sure appointment_id is set
    }
    return render(request, 'home_doc.html', context)

@login_required
def vaccine_bookings(request):
    # Ensure the user is associated with a hospital
    if hasattr(request.user, 'hospital'):
        hospital = request.user.hospital
        # Filter vaccine bookings by the hospital
        vaccinations = Vaccination.objects.filter(hospital=hospital).order_by('-next_vaccination_date')

        return render(request, 'vaccine_bookings.html', {'vaccinations': vaccinations})
    else:
        return redirect('hospital_login')  # Redirect to login if not associated with any hospital


def doctor_profile(request):
    return render(request, 'doctor-profile.html')