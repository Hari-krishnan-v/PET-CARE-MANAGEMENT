from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile),
    path('treatment', views.treatment),
    path('blank', views.blank),
    path('contact', views.contact),
    path('error', views.error),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
]