from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'home.html')

def login(request):
    return render(request,'pages-login.html')

def treatment(request):
    return render(request,'Treatment.html')

def profile(request):
    return render(request,'users-profile.html')

def blank(request):
    return render(request,'pages-blank.html')

def contact(request):
    return render(request,'pages-contact.html')

def error(request):
    return render(request,'pages-error-404.html')