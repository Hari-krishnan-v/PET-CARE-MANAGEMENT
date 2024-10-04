# user/views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
from .forms import AppointmentForm, VaccinationBookingForm
from datetime import date, timedelta
from django.utils import timezone
from django.urls import reverse
from django.views.decorators.http import require_POST
# models
from .models import PetProfile ,Notification,Hospital,Appointment,Customer, Vaccination
from doctor.models import Prescription,Medicine


def login_view(request):
    context = {}
    if request.method == 'POST':
        if 'register' in request.POST:
            context['register'] = True
           
            try: 
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                address = request.POST.get('address')
                phone = request.POST.get('phone')
                pet_name = request.POST['pet_name']
                pet_birthdate = request.POST['pet_birthdate']
                pet_type = request.POST['pet_type']

                if User.objects.filter(username=username).exists():
                    context['toastr_message'] = "Username already taken"
                    context['toastr_type'] = "error"
                elif User.objects.filter(email=email).exists():
                    context['toastr_message'] = "Email already taken"
                    context['toastr_type'] = "error"
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                    )
                    customer = Customer.objects.create(
                        user=user,
                        phone=phone,
                        address=address
                    )
                    pet_profile = PetProfile.objects.create(
                        user=user,
                        pet_name=pet_name,
                        pet_birthdate=pet_birthdate,
                        pet_type=pet_type
                    )
                    context['toastr_message'] = "User registered successfully"
                    context['toastr_type'] = "success"
            except IntegrityError:
                context['toastr_message'] = "Duplicate username or invalid credentials"
                context['toastr_type'] = "error"
            except Exception as e:
                context['toastr_message'] = str(e)
                context['toastr_type'] = "error"
        elif 'login' in request.POST:
            context['register'] = False
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                # Set success message for Toastr
                context['toastr_message'] = 'Logged in successfully'
                context['toastr_type'] = 'success'
                return redirect('home')
            else:
                context['toastr_message'] = 'Invalid username or password'
                context['toastr_type'] = 'error'

    return render(request, 'login.html', context)


def calculate_next_vaccination_date(pet_type, pet_birthdate):
    today = date.today()
    age_in_days = (today - pet_birthdate).days

    vaccine_schedule = {
        'dog': [
            (56, 'Distemper'),
            (70, 'Parvovirus'),
            (84, 'Adenovirus'),
            (98, 'Parainfluenza'),
            (365, 'Rabies'),
            (365, 'Leptospirosis'),
            (365, 'Bordetella (Kennel Cough)'),
        ],
        'cat': [
            (56, 'Feline Viral Rhinotracheitis (FVR)'),
            (70, 'Feline Calicivirus (FCV)'),
            (84, 'Feline Panleukopenia (FPV)'),
            (98, 'Chlamydia'),
            (365, 'Rabies'),
            (365, 'Feline Leukemia (FeLV)'),
        ],
        'bird': [
            (56, 'Polyomavirus'),
            (365, 'Pacheco\'s Disease'),
            (365, 'Psittacine Beak and Feather Disease (PBFD)'),
        ],
    }

    for days, vaccine_name in vaccine_schedule.get(pet_type, []):
        if age_in_days < days:
            next_vaccination_date = pet_birthdate + timedelta(days=days)
            return next_vaccination_date, vaccine_name

    return today + timedelta(days=365), 'Annual Vaccine'

@login_required
def vaccination_appointment_view(request, date):
    user = request.user
    try:
        pet_profile = PetProfile.objects.get(user=user)
    except PetProfile.DoesNotExist:
        return redirect('profile')

    pet_type = pet_profile.pet_type
    pet_birthdate = pet_profile.pet_birthdate
    next_vaccination_date, vaccine_name = calculate_next_vaccination_date(pet_type, pet_birthdate)

    if request.method == 'POST':
        form = VaccinationBookingForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.user = request.user
            vaccination.next_vaccination_date = next_vaccination_date
            vaccination.due_date = next_vaccination_date
            vaccination.booking_date = timezone.now().date()
            vaccination.save()

            messages.success(request, 'Vaccination appointment booked successfully!')
            return redirect('vaccination_appointment', date=date)  # Correct URL name

    else:
        form = VaccinationBookingForm(initial={
            'vaccine_name': vaccine_name,
            'next_vaccination_date': next_vaccination_date,
            'due_date': next_vaccination_date,
        })

    hospitals = Hospital.objects.all()
    return render(request, 'vaccination_booking.html', {'form': form, 'hospitals': hospitals, 'next_vaccination_date': next_vaccination_date})

require_POST
def undo_vaccination(request):
    appointment_id = request.POST.get('id')
    if appointment_id:
        try:
            Vaccination.objects.filter(id=appointment_id).delete()
            return JsonResponse({'status': 'success'})
        except Vaccination.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid data'})

@login_required
def home(request):
    user = request.user

    try:
        pet_profile = PetProfile.objects.get(user=user)
    except PetProfile.DoesNotExist:
        messages.error(request, 'Pet profile not found. Please update your profile.')
        pet_profile = None
        next_vaccination_date = None
        vaccine_name = None
        notifications = []  
        medicine_count = 0 
        prescription_count = 0  
    else:
        
        prescription_count = Prescription.objects.filter(appointment__user=user).count()
        
       
        next_vaccination_date, vaccine_name = calculate_next_vaccination_date(pet_profile.pet_type, pet_profile.pet_birthdate)
        notification_date = next_vaccination_date - timedelta(days=3)
        today = timezone.now().date()
        notifications = []  

        if today >= notification_date and today < next_vaccination_date:
            notifications.append({
                'title': 'Vaccination Reminder',
                'message': f'Next vaccination ({vaccine_name}) is due on {next_vaccination_date.strftime("%d %b %Y")}.',
                'time': 'Just now'
            })

        latest_prescription = Prescription.objects.filter(appointment__user=user).order_by('-date').first()
        medicine_count = latest_prescription.medicines.count() if latest_prescription else 0

    notifications += Notification.objects.filter(user=user, read=False)

    context = {
        'prescription_count': prescription_count,
        'pet_profile': pet_profile,
        'next_vaccination_date': next_vaccination_date,
        'notifications': notifications,
        'vaccine_name': vaccine_name,
        'medicine_count': medicine_count,
    }
    return render(request, 'home.html', context)

@login_required
def clear_all_notifications(request):
    user = request.user
    Notification.objects.filter(user=user, read=False).delete()
    messages.success(request, 'All notifications have been cleared.')
    return redirect('home')



def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')



@login_required
def book_appointment(request):
    if request.method == 'POST':
        if 'undo' in request.POST:
            undo_data = request.session.pop('undo_appointment', None)
            if undo_data:
                Appointment.objects.filter(id=undo_data['id']).delete()
                messages.info(request, 'Appointment booking undone.')
            return redirect(reverse('book_appointment'))

        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            try:
                pet_profile = PetProfile.objects.get(user=request.user)
                appointment.pet_profile = pet_profile
                appointment.name = pet_profile.pet_name
                appointment.email = request.user.email
                appointment.phone = request.user.customer.phone if hasattr(request.user, 'customer') else 'No Phone'
                appointment.pet_type = pet_profile.pet_type
            except PetProfile.DoesNotExist:
                messages.error(request, 'Pet profile not found. Please update your profile.')
                return redirect(reverse('book_appointment'))

            appointment.save()
            request.session['undo_appointment'] = {
                'id': appointment.id,
                'name': appointment.name,
                'email': appointment.email,
                'phone': appointment.phone,
                'pet_type': appointment.pet_type,
            }
            messages.success(request, 'Appointment booked successfully!')

    else:
        try:
            pet_profile = PetProfile.objects.get(user=request.user)
            initial_data = {
                'name': pet_profile.pet_name,
                'email': request.user.email,
                'phone': request.user.customer.phone if hasattr(request.user, 'customer') else 'No Phone',
                'treatment_type': 'grooming',
                'hospital': None,
                'notes': '',
            }
            form = AppointmentForm(initial=initial_data)
        except PetProfile.DoesNotExist:
            form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})


def training_centers(request):
    return render(request, 'training_centers.html')


@login_required
def profile(request):
    user = request.user

    try:
        customer = user.customer
        pet_profile, created = PetProfile.objects.get_or_create(user=user)  # Ensure pet_profile is created if not exists
    except PetProfile.DoesNotExist:
        messages.error(request, 'Pet profile not found. Please update your profile.')
        pet_profile = None  

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pet_birthdate = request.POST.get('pet_birthdate')

        print(pet_name)
        print(pet_type)
        print(address)
        print(phone)
        print(pet_birthdate)

        if pet_profile:
            if pet_name:
                pet_profile.pet_name = pet_name
            if pet_type:
                pet_profile.pet_type = pet_type
            if pet_birthdate:
                pet_profile.pet_birthdate = pet_birthdate
            pet_profile.save()

        customer.address = address
        customer.phone = phone
        customer.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {
        'user': user,
        'customer': customer,
        'pet_profile': pet_profile,
    }
    return render(request, 'users-profile.html', context)

@login_required
def update_settings(request):
    user = request.user
    customer = user.customer

    if request.method == 'POST':
        email_notifications = request.POST.get('email_notifications')
        customer.email_notifications = bool(email_notifications)
        customer.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('profile')

    return render(request, 'user_profile.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user_profile.html', {'form': form})



def blank(request):
    return render(request,'pages-blank.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject,
                full_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent. Thank you!')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
        
        return redirect('contact')

    return render(request, 'pages-contact.html')

def faq(request):
    return render(request,'faq.html')

@login_required
def latest_prescription(request):
    
    latest_prescription = Prescription.objects.filter(appointment__user=request.user).order_by('-date').first()

    if latest_prescription:
        
        medicines = latest_prescription.medicines.all()
    else:
        
        medicines = Medicine.objects.none()

    context = {
        'latest_prescription': latest_prescription,
        'medicines': medicines,
        'prescription_date': latest_prescription.date if latest_prescription else None,
        'doctor_name': latest_prescription.hospital.name if latest_prescription and latest_prescription.hospital else 'N/A',
        'medicine_count': medicines.count() if latest_prescription else 0,
    }
    return render(request, 'latest_prescription.html', context)
@login_required
def prescription_history(request):
    # Filter prescriptions based on the user through the related appointment
    prescriptions = Prescription.objects.filter(appointment__user=request.user).order_by('-date')
    return render(request, 'prescription_history.html', {'prescriptions': prescriptions})

@login_required
def clear_prescriptions(request):
    user = request.user
    # Filter prescriptions where the related appointment's user is the current user
    Prescription.objects.filter(appointment__user=user).delete()
    messages.success(request, 'All previous prescriptions have been cleared.')
    return redirect('prescription_history')