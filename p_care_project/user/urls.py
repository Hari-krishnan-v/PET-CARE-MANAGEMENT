from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('contact/profile/', views.profile, name='profile'), 
    path('blank/', views.blank, name='blank'),
    path('contact/', views.contact, name='contact'),
    path('error/', views.error, name='error'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/contact/', views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)