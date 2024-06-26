from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.core.mail import send_mail
from django.conf import settings
from .forms import AppointmentForm
from .models import Appointment ,Vaccination
from .models import PetProfile
from datetime import date, timedelta
from django.utils import timezone

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

    if pet_type == 'dog':
        if age_in_days < 56:
            return pet_birthdate + timedelta(days=56)
        elif 56 <= age_in_days < 70:
            return pet_birthdate + timedelta(days=70)
        elif 70 <= age_in_days < 84:
            return pet_birthdate + timedelta(days=84)
        elif 84 <= age_in_days < 98:
            return pet_birthdate + timedelta(days=98)
        else:
            return today + timedelta(days=365)
    elif pet_type == 'cat':
        if age_in_days < 56:
            return pet_birthdate + timedelta(days=56)
        elif 56 <= age_in_days < 70:
            return pet_birthdate + timedelta(days=70)
        elif 70 <= age_in_days < 84:
            return pet_birthdate + timedelta(days=84)
        elif 84 <= age_in_days < 98:
            return pet_birthdate + timedelta(days=98)
        else:
            return today + timedelta(days=365)
    elif pet_type == 'bird':
        if age_in_days < 56:
            return pet_birthdate + timedelta(days=56)
        else:
            return today + timedelta(days=365)
    else:
        return None

@login_required
def home(request):
    user = request.user
    pet_profile = PetProfile.objects.get(user=user)
    next_vaccination_date = calculate_next_vaccination_date(pet_profile.pet_type, pet_profile.pet_birthdate)

    # Calculate the notification date
    notification_date = next_vaccination_date - timedelta(days=3)

    # Check if today is the notification date
    today = timezone.now().date()
    notifications = []
    if today >= notification_date and today < next_vaccination_date:
        notifications.append({
            'title': 'Vaccination Reminder',
            'message': f'Next vaccination is due on {next_vaccination_date.strftime("%d %b %Y")}.',
            'time': 'Just now'
        })

    context = {
        'pet_profile': pet_profile,
        'next_vaccination_date': next_vaccination_date,
        'notifications': notifications,
    }
    return render(request, 'home.html', context)

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
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('home')
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})

@login_required
def vaccination_appointment_view(request):
    if request.method == "POST":
        # Handle the appointment booking logic here
        pass
    return render(request, 'vaccination_appointment.html')

def profile(request):
    return render(request,'users-profile.html')

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