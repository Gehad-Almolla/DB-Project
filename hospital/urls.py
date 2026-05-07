from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    # Home and Auth
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('patient/register/', views.patient_register, name='patient_register'),
    path('doctor/register/', views.doctor_register, name='doctor_register'),
    
    # Patient URLs
    path('patient/profile/setup/', views.patient_profile_setup, name='patient_profile_setup'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patient/profile/', views.patient_profile, name='patient_profile'),
    path('patient/appointments/', views.patient_appointments, name='patient_appointments'),
    path('patient/appointment/book/', views.book_appointment, name='book_appointment'),
    path('patient/appointment/<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
    path('patient/appointment/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('patient/medical-records/', views.patient_medical_records, name='patient_medical_records'),
    path('patient/prescriptions/', views.patient_prescriptions, name='patient_prescriptions'),
    path('patient/scans/', views.patient_scans, name='patient_scans'),
    
    # Doctor URLs
    path('doctor/profile/setup/', views.doctor_profile_setup, name='doctor_profile_setup'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('doctor/patients/', views.doctor_patients, name='doctor_patients'),
    path('doctor/patient/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('doctor/patient/<int:patient_pk>/medical-record/add/', views.add_medical_record, name='add_medical_record'),
    path('doctor/patient/<int:patient_pk>/prescription/add/', views.add_prescription, name='add_prescription'),
    path('doctor/patient/<int:patient_pk>/scan/upload/', views.upload_scan, name='upload_scan'),
    
    # Public URLs
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', views.about_us, name='about_us'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
