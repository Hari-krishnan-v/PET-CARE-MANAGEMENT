# user/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.core.mail import send_mail
from django.conf import settings
from .forms import AppointmentForm, VaccinationBookingForm
from .models import Appointment ,Vaccination ,PetProfile ,Notification
from datetime import date, timedelta
from django.utils import timezone
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from doctor.models import Prescription

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
                    messages.error(request, "Username already taken")
                elif User.objects.filter(email=email).exists():
                    messages.error(request, "Email already taken")
                else:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        email=email
                    )
                    customer = Customer.objects.create(
                        user=user,
                        phone=phone,
                        address=address,
                      
                       
                    )
                    customer.save()
                    pet_profile = PetProfile.objects.create(
                        user=user,
                        pet_name=pet_name,
                        pet_birthdate=pet_birthdate,
                        pet_type=pet_type
                    )
                    pet_profile.save()
                    messages.success(request, "User registered successfully")
            except IntegrityError:
                messages.error(request, "Duplicate username or invalid credentials")
            except Exception as e:
                messages.error(request, str(e))
        elif 'login' in request.POST:
            context['register'] = False
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')

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
def vaccination_appointment_view(request, next_vaccination_date):
    user = request.user

    try:
        pet_profile = PetProfile.objects.get(user=user)
    except PetProfile.DoesNotExist:
        messages.error(request, 'Pet profile not found. Please update your profile.')
        return redirect('profile')  # Or redirect to a suitable page

    next_vaccination_date, vaccine_name = calculate_next_vaccination_date(pet_profile.pet_type, pet_profile.pet_birthdate)
    due_date = next_vaccination_date

    if request.method == 'POST':
        form = VaccinationBookingForm(request.POST)
        if form.is_valid():
            vaccination = form.save(commit=False)
            vaccination.user = request.user
            vaccination.save()
            messages.success(request, 'Vaccination appointment booked successfully!')
            return redirect('home')  # Or any other page you want to redirect to
    else:
        form = VaccinationBookingForm(initial={
            'vaccine_name': vaccine_name,
            'next_vaccination_date': next_vaccination_date,
            'due_date': due_date,
        })

    return render(request, 'vaccination_booking.html', {'form': form, 'next_vaccination_date': next_vaccination_date})


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
        notifications = []  # Ensure notifications is always defined
        medicine_count = 0  # Default value when pet profile is missing
    else:
        prescription_count = Prescription.objects.filter(patient=request.user).count()
        next_vaccination_date, vaccine_name = calculate_next_vaccination_date(pet_profile.pet_type, pet_profile.pet_birthdate)
        notification_date = next_vaccination_date - timedelta(days=3)
        today = timezone.now().date()
        notifications = []  # Initialize notifications list

        if today >= notification_date and today < next_vaccination_date:
            notifications.append({
                'title': 'Vaccination Reminder',
                'message': f'Next vaccination ({vaccine_name}) is due on {next_vaccination_date.strftime("%d %b %Y")}.',
                'time': 'Just now'
            })

        # Get the latest prescription and its medicine count
        latest_prescription = Prescription.objects.filter(patient=request.user).order_by('-date').first()
        medicine_count = latest_prescription.medicines.count() if latest_prescription else 0

    # Fetch unread notifications
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
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user_id = request.user.id

            # Retrieve the pet profile and set the pet_type
            try:
                pet_profile = PetProfile.objects.get(user=request.user)
                appointment.pet_type = pet_profile.pet_type
            except PetProfile.DoesNotExist:
                # Handle the case where PetProfile does not exist
                messages.error(request, 'Pet profile not found. Please update your profile.')
                return redirect('profile')

            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            
    else:
        form = AppointmentForm()
    
    return render(request, 'book_appointment.html', {'form': form})



@login_required
def profile(request):
    user = request.user

    try:
        customer = user.customer
        pet_profile = PetProfile.objects.get(user=user)
    except PetProfile.DoesNotExist:
        messages.error(request, 'Pet profile not found. Please update your profile.')
        pet_profile = None  # or handle this case appropriately

    if request.method == 'POST':
        pet_name = request.POST.get('pet_name')
        pet_type = request.POST.get('pet_type')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pet_birthdate = request.POST.get('pet_birthdate')

        if pet_profile:
            pet_profile.pet_name = pet_name
            pet_profile.pet_type = pet_type
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
            update_session_auth_hash(request, user)  # Important to maintain session
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

def latest_prescription(request):
    latest_prescription = Prescription.objects.filter(patient=request.user).order_by('-date').first()
    medicine_count = latest_prescription.medicines.count() if latest_prescription else 0

    if latest_prescription:
        # Access the hospital associated with the prescription
        hospital = latest_prescription.hospital
        doctor_name = hospital.name  # Assuming the hospital's name represents the doctor
    else:
        doctor_name = 'No doctor assigned'  # Handle case when there is no prescription

    return render(request, 'latest_prescription.html', {
        'prescription': latest_prescription,
        'medicine_count': medicine_count,
        'doctor_name': doctor_name
    })

@login_required
def prescription_history(request):
    prescriptions = Prescription.objects.filter(patient=request.user).order_by('-date')
    return render(request, 'prescription_history.html', {'prescriptions': prescriptions})

@login_required
def clear_prescriptions(request):
    user = request.user
    Prescription.objects.filter(patient=user).delete()
    messages.success(request, 'All previous prescriptions have been cleared.')
    return redirect('prescription_history')