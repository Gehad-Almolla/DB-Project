from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.http import JsonResponse
from datetime import datetime, timedelta
import uuid

from .models import (
    Patient, Doctor, Department, Appointment, Room, Prescription,
    RoomReservation, ContactInquiry, MedicalRecord, PaymentRecord, ScanDocument
)
from .forms import (
    PatientRegistrationForm, PatientProfileForm, DoctorRegistrationForm,
    DoctorProfileForm, AppointmentForm, PrescriptionForm, ContactInquiryForm,
    MedicalRecordForm, ScanDocumentForm, UserUpdateForm, AppointmentCancellationForm,
    PaymentForm
)
from django.contrib.auth.models import User


# ============== HOME AND AUTHENTICATION ==============

def home(request):
    """Home Page"""
    doctors = Doctor.objects.select_related('department').all()[:6]
    context = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'featured_doctors': doctors,
    }
    return render(request, 'hospital/home.html', context)


def patient_register(request):
    """Patient Registration"""
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('patient_profile_setup')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = PatientRegistrationForm()
    
    return render(request, 'hospital/patient_register.html', {'form': form})


def doctor_register(request):
    """Doctor Registration"""
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Please complete your profile.')
            return redirect('doctor_profile_setup')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'hospital/doctor_register.html', {'form': form})


def login_view(request):
    """Login View"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to appropriate dashboard
            if hasattr(user, 'patient_profile'):
                return redirect('patient_dashboard')
            elif hasattr(user, 'doctor_profile'):
                return redirect('doctor_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'hospital/login.html')


@login_required
def logout_view(request):
    """Logout View"""
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


# ============== PATIENT VIEWS ==============

@login_required
def patient_profile_setup(request):
    """Complete Patient Profile After Registration"""
    try:
        patient = request.user.patient_profile
        return redirect('patient_dashboard')
    except Patient.DoesNotExist:
        if request.method == 'POST':
            form = PatientProfileForm(request.POST, request.FILES)
            if form.is_valid():
                patient = form.save(commit=False)
                patient.user = request.user
                patient.save()
                messages.success(request, 'Profile setup completed!')
                return redirect('patient_dashboard')
        else:
            form = PatientProfileForm()
        
        return render(request, 'hospital/patient_profile_setup.html', {'form': form})


@login_required
def patient_dashboard(request):
    """Patient Dashboard"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    upcoming_appointments = patient.appointments.filter(
        appointment_date__gte=timezone.now(),
        status__in=['SCHEDULED', 'CONFIRMED']
    ).order_by('appointment_date')[:5]
    
    past_appointments = patient.appointments.filter(
        status='COMPLETED'
    ).order_by('-appointment_date')[:5]
    
    context = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'total_appointments': patient.appointments.count(),
        'medical_records': patient.medical_records.all()[:5],
    }
    return render(request, 'hospital/patient_dashboard.html', context)


@login_required
def book_appointment(request):
    """Book Appointment"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user.patient_profile
            appointment.cost = appointment.doctor.consultation_fee
            appointment.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('patient_appointments')
    else:
        form = AppointmentForm()
    
    context = {'form': form, 'doctors': Doctor.objects.all()}
    return render(request, 'hospital/book_appointment.html', context)


@login_required
def patient_appointments(request):
    """View Patient Appointments"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    status_filter = request.GET.get('status', 'all')
    
    appointments = patient.appointments.all().order_by('-appointment_date')
    
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'hospital/patient_appointments.html', context)


@login_required
def cancel_appointment(request, pk):
    """Cancel Appointment"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    if appointment.patient.user != request.user:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    if appointment.status not in ['SCHEDULED', 'CONFIRMED']:
        messages.error(request, 'This appointment cannot be cancelled.')
        return redirect('patient_appointments')
    
    if request.method == 'POST':
        form = AppointmentCancellationForm(request.POST)
        if form.is_valid():
            appointment.status = 'CANCELLED'
            appointment.notes = form.cleaned_data.get('reason', '')
            appointment.save()
            messages.success(request, 'Appointment cancelled successfully.')
            return redirect('patient_appointments')
    else:
        form = AppointmentCancellationForm()
    
    return render(request, 'hospital/cancel_appointment.html', {'appointment': appointment, 'form': form})


@login_required
def patient_medical_records(request):
    """View Patient Medical Records"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    records = patient.medical_records.all().order_by('-record_date')
    
    context = {'records': records}
    return render(request, 'hospital/patient_medical_records.html', context)


@login_required
def patient_prescriptions(request):
    """View Patient Prescriptions"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    prescriptions = patient.prescriptions.all().order_by('-prescription_date')
    
    context = {'prescriptions': prescriptions}
    return render(request, 'hospital/patient_prescriptions.html', context)


@login_required
def patient_scans(request):
    """View Patient Scans"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    scans = patient.scans.all().order_by('-scan_date')
    
    context = {'scans': scans}
    return render(request, 'hospital/patient_scans.html', context)


@login_required
def patient_profile(request):
    """View/Edit Patient Profile"""
    if not hasattr(request.user, 'patient_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = request.user.patient_profile
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        patient_form = PatientProfileForm(request.POST, request.FILES, instance=patient)
        
        if user_form.is_valid() and patient_form.is_valid():
            user_form.save()
            patient_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('patient_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        patient_form = PatientProfileForm(instance=patient)
    
    context = {'user_form': user_form, 'patient_form': patient_form}
    return render(request, 'hospital/patient_profile.html', context)


# ============== DOCTOR VIEWS ==============

@login_required
def doctor_profile_setup(request):
    """Complete Doctor Profile After Registration"""
    try:
        doctor = request.user.doctor_profile
        return redirect('doctor_dashboard')
    except Doctor.DoesNotExist:
        if request.method == 'POST':
            form = DoctorProfileForm(request.POST, request.FILES)
            if form.is_valid():
                doctor = form.save(commit=False)
                doctor.user = request.user
                doctor.save()
                messages.success(request, 'Profile setup completed!')
                return redirect('doctor_dashboard')
        else:
            form = DoctorProfileForm()
        
        return render(request, 'hospital/doctor_profile_setup.html', {'form': form})


@login_required
def doctor_dashboard(request):
    """Doctor Dashboard"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = request.user.doctor_profile
    today = timezone.now().date()
    
    today_appointments = doctor.appointments.filter(
        appointment_date__date=today,
        status__in=['SCHEDULED', 'CONFIRMED']
    ).order_by('appointment_date')
    
    upcoming_appointments = doctor.appointments.filter(
        appointment_date__gte=timezone.now(),
        status__in=['SCHEDULED', 'CONFIRMED']
    ).order_by('appointment_date')[:10]
    
    context = {
        'doctor': doctor,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'total_patients': doctor.appointments.values('patient').distinct().count(),
        'total_appointments': doctor.appointments.count(),
    }
    return render(request, 'hospital/doctor_dashboard.html', context)


@login_required
def doctor_appointments(request):
    """View Doctor's Appointments"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = request.user.doctor_profile
    status_filter = request.GET.get('status', 'all')
    
    appointments = doctor.appointments.all().order_by('-appointment_date')
    
    if status_filter != 'all':
        appointments = appointments.filter(status=status_filter)
    
    context = {
        'appointments': appointments,
        'status_filter': status_filter,
    }
    return render(request, 'hospital/doctor_appointments.html', context)


@login_required
def doctor_patients(request):
    """View Doctor's Patients"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    doctor = request.user.doctor_profile
    patients = Patient.objects.filter(
        appointments__doctor=doctor
    ).distinct().prefetch_related('medical_records', 'prescriptions')
    
    context = {'patients': patients}
    return render(request, 'hospital/doctor_patients.html', context)


@login_required
def patient_detail(request, pk):
    """View Patient Details (Doctor View)"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = get_object_or_404(Patient, pk=pk)
    doctor = request.user.doctor_profile
    
    # Verify doctor has appointments with this patient
    if not doctor.appointments.filter(patient=patient).exists():
        messages.error(request, 'Access denied.')
        return redirect('doctor_patients')
    
    medical_records = patient.medical_records.all().order_by('-record_date')
    prescriptions = patient.prescriptions.filter(doctor=doctor).order_by('-prescription_date')
    scans = patient.scans.all().order_by('-scan_date')
    
    context = {
        'patient': patient,
        'medical_records': medical_records,
        'prescriptions': prescriptions,
        'scans': scans,
    }
    return render(request, 'hospital/patient_detail.html', context)


@login_required
def add_medical_record(request, patient_pk):
    """Add Medical Record (Doctor)"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    doctor = request.user.doctor_profile
    
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.recorded_by = doctor
            record.save()
            messages.success(request, 'Medical record added successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = MedicalRecordForm()
    
    return render(request, 'hospital/add_medical_record.html', {'form': form, 'patient': patient})


@login_required
def add_prescription(request, patient_pk):
    """Add Prescription (Doctor)"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    doctor = request.user.doctor_profile
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor
            prescription.patient = patient
            prescription.save()
            messages.success(request, 'Prescription created successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PrescriptionForm()
    
    return render(request, 'hospital/add_prescription.html', {'form': form, 'patient': patient})


@login_required
def upload_scan(request, patient_pk):
    """Upload Patient Scan (Doctor)"""
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    patient = get_object_or_404(Patient, pk=patient_pk)
    doctor = request.user.doctor_profile
    
    if request.method == 'POST':
        form = ScanDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.patient = patient
            scan.doctor = doctor
            scan.save()
            messages.success(request, 'Scan uploaded successfully!')
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = ScanDocumentForm()
    
    return render(request, 'hospital/upload_scan.html', {'form': form, 'patient': patient})


# ============== PUBLIC VIEWS ==============

def doctors_list(request):
    """List All Doctors"""
    specialty = request.GET.get('specialty', '')
    search = request.GET.get('search', '')
    
    doctors = Doctor.objects.select_related('department').all()
    
    if specialty:
        doctors = doctors.filter(specialty=specialty)
    
    if search:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(bio__icontains=search)
        )
    
    specialties = Doctor.SPECIALTIES
    
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'search': search,
        'specialty': specialty,
    }
    return render(request, 'hospital/doctors_list.html', context)


def doctor_detail(request, pk):
    """Doctor Detail View"""
    doctor = get_object_or_404(Doctor, pk=pk)
    context = {'doctor': doctor}
    return render(request, 'hospital/doctor_detail.html', context)


def contact_us(request):
    """Contact Form"""
    if request.method == 'POST':
        form = ContactInquiryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your inquiry has been submitted. We will contact you soon.')
            return redirect('home')
    else:
        form = ContactInquiryForm()
    
    return render(request, 'hospital/contact_us.html', {'form': form})


def about_us(request):
    """About Us Page"""
    department = Department.objects.first()
    context = {'department': department}
    return render(request, 'hospital/about_us.html', context)


# ============== ADMIN VIEWS ==============

@login_required
def admin_dashboard(request):
    """Admin Dashboard"""
    if not request.user.is_staff:
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_appointments': Appointment.objects.count(),
        'total_revenue': PaymentRecord.objects.filter(status='COMPLETED').aggregate(Sum('amount'))['amount__sum'] or 0,
        'recent_inquiries': ContactInquiry.objects.all()[:10],
        'pending_inquiries': ContactInquiry.objects.filter(is_responded=False).count(),
    }
    return render(request, 'hospital/admin_dashboard.html', context)


@login_required
def appointment_detail(request, pk):
    """View Appointment Details"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Check permissions
    is_patient = hasattr(request.user, 'patient_profile') and appointment.patient.user == request.user
    is_doctor = hasattr(request.user, 'doctor_profile') and appointment.doctor.user == request.user
    is_staff = request.user.is_staff
    
    if not (is_patient or is_doctor or is_staff):
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    context = {'appointment': appointment}
    return render(request, 'hospital/appointment_detail.html', context)
