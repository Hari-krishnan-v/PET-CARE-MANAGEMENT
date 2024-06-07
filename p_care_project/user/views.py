from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import Customer
from django.core.mail import send_mail
from django.conf import settings


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
                profile_image = request.FILES.get('profile_image')

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
                        profile_image=profile_image
                    )
                    customer.save()
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

@login_required
def home(request):
    return render(request, 'home.html', {'section': 'home'})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')






def treatment(request):
    return render(request,'Treatment.html')

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

def error(request):
    return render(request,'pages-error-404.html')