from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_views
from .views import vaccination_appointment_view ,latest_prescription, prescription_history


urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('latest_prescription/', latest_prescription, name='latest_prescription'),
    path('prescription_history/', prescription_history, name='prescription_history'),
    path('clear_prescriptions/', views.clear_prescriptions, name='clear_prescriptions'),
    re_path(r'^vaccination_appointment/(?P<date>\d{4}-\d{2}-\d{2})/$', vaccination_appointment_view, name='vaccination_appointment'),
    path('undo-vaccination/', views.undo_vaccination, name='undo_vaccination'),
    path('training-centers/', views.training_centers, name='training_centers'),
    path('contact/profile/', views.profile, name='profile'),
    path('blank/', views.blank, name='blank'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('clear_all_notifications/', views.clear_all_notifications, name='clear_all_notifications'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('update_settings/', views.update_settings, name='update_settings'),
    path('change_password/', views.change_password, name='change_password'),
    path('contact/contact/', views.contact, name='contact'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)