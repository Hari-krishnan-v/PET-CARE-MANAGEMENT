from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home),
    path('home', views.home),
    path('profile', views.profile),
    path('treatment', views.treatment),
    path('blank', views.blank),
    path('contact', views.contact),
    path('error', views.error),
]