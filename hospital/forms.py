from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Patient, Doctor, Appointment, Prescription, RoomReservation, 
    ContactInquiry, MedicalRecord, ScanDocument, PaymentRecord
)
from datetime import datetime, timedelta


class PatientRegistrationForm(UserCreationForm):
    """Patient Registration Form"""
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        # Use email as username when possible; fall back to first+last, ensure uniqueness
        base_username = (self.cleaned_data.get('email') or '').split('@')[0] or (
            (self.cleaned_data.get('first_name') or '') + (self.cleaned_data.get('last_name') or '')
        )
        base_username = base_username.strip() or 'user'
        username = base_username
        from django.contrib.auth.models import User
        counter = 0
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}{counter}"

        user.username = username
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user
    
    def save(self, commit=True):
        user = super().save(commit=False)
        base_username = (self.cleaned_data.get('email') or '').split('@')[0] or (
            (self.cleaned_data.get('first_name') or '') + (self.cleaned_data.get('last_name') or '')
        )
        base_username = base_username.strip() or 'user'
        username = base_username
        from django.contrib.auth.models import User
        counter = 0
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}{counter}"

        user.username = username
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


class PatientProfileForm(forms.ModelForm):
    """Patient Profile Form"""
    class Meta:
        model = Patient
        fields = ('patient_number', 'social_security_number', 'phone', 'address', 
                  'birthdate', 'gender', 'blood_type', 'medical_history', 
                  'emergency_contact', 'emergency_phone', 'profile_photo')
        widgets = {
            'patient_number': forms.TextInput(attrs={'class': 'form-control'}),
            'social_security_number': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_type': forms.Select(attrs={'class': 'form-control'}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_patient_number(self):
        patient_number = self.cleaned_data.get('patient_number', '').strip()
        if not patient_number:
            # Auto-generate patient number
            import uuid
            patient_number = f"PAT-{uuid.uuid4().hex[:8].upper()}"
        
        # Check uniqueness
        existing = Patient.objects.filter(patient_number=patient_number)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("This patient number already exists. Please enter a unique one.")
        
        return patient_number
    
    def clean_social_security_number(self):
        ssn = self.cleaned_data.get('social_security_number', '').strip()
        if not ssn:
            # Auto-generate SSN-like identifier
            import uuid
            ssn = f"SSN-{uuid.uuid4().hex[:8].upper()}"
        
        # Check uniqueness
        existing = Patient.objects.filter(social_security_number=ssn)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("This social security number already exists.")
        
        return ssn


class DoctorRegistrationForm(UserCreationForm):
    """Doctor Registration Form"""
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class DoctorProfileForm(forms.ModelForm):
    """Doctor Profile Form"""
    class Meta:
        model = Doctor
        fields = ('license_number', 'social_security_number', 'birthdate', 'gender',
                  'specialty', 'degree', 'department', 'office_location', 'bio',
                  'consultation_fee', 'qualification_document', 'profile_photo')
        widgets = {
            'license_number': forms.TextInput(attrs={'class': 'form-control'}),
            'social_security_number': forms.TextInput(attrs={'class': 'form-control'}),
            'birthdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'specialty': forms.Select(attrs={'class': 'form-control'}),
            'degree': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'office_location': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'consultation_fee': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'qualification_document': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def clean_license_number(self):
        license_number = self.cleaned_data.get('license_number', '').strip()
        if not license_number:
            # Auto-generate license number
            import uuid
            license_number = f"LIC-{uuid.uuid4().hex[:8].upper()}"
        
        # Check uniqueness
        existing = Doctor.objects.filter(license_number=license_number)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("This license number already exists. Please enter a unique one.")
        
        return license_number
    
    def clean_social_security_number(self):
        ssn = self.cleaned_data.get('social_security_number', '').strip()
        if not ssn:
            # Auto-generate SSN-like identifier
            import uuid
            ssn = f"SSN-{uuid.uuid4().hex[:8].upper()}"
        
        # Check uniqueness
        existing = Doctor.objects.filter(social_security_number=ssn)
        if self.instance and self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("This social security number already exists.")
        
        return ssn


class AppointmentForm(forms.ModelForm):
    """Appointment Booking Form"""
    doctor = forms.ModelChoiceField(
        queryset=Doctor.objects.filter(department__name='Surgery Department'),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Select Doctor'
    )
    
    class Meta:
        model = Appointment
        fields = ('doctor', 'appointment_date', 'duration_minutes', 'reason_for_visit', 'notes')
        widgets = {
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.Select(
                choices=[(30, '30 mins'), (45, '45 mins'), (60, '1 hour'), (90, '1.5 hours')],
                attrs={'class': 'form-control'}
            ),
            'reason_for_visit': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }
    
    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < datetime.now():
            raise forms.ValidationError("Appointment date must be in the future.")
        return appointment_date


class PrescriptionForm(forms.ModelForm):
    """Prescription Form"""
    class Meta:
        model = Prescription
        fields = ('medication_name', 'dosage', 'frequency', 'start_date', 'end_date',
                  'instructions', 'quantity', 'refills_remaining')
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 500mg'}),
            'frequency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2 times daily'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'refills_remaining': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RoomReservationForm(forms.ModelForm):
    """Room Reservation Form"""
    class Meta:
        model = RoomReservation
        fields = ('room', 'check_in_date', 'check_out_date', 'reason')
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'check_in_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'check_out_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ContactInquiryForm(forms.ModelForm):
    """Contact Inquiry Form"""
    class Meta:
        model = ContactInquiry
        fields = ('name', 'email', 'phone', 'inquiry_type', 'message', 'attachment')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'inquiry_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MedicalRecordForm(forms.ModelForm):
    """Medical Record Form"""
    class Meta:
        model = MedicalRecord
        fields = ('blood_pressure', 'heart_rate', 'temperature', 'weight', 'height', 'notes')
        widgets = {
            'blood_pressure': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '120/80'}),
            'heart_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ScanDocumentForm(forms.ModelForm):
    """Scan Document Upload Form"""
    class Meta:
        model = ScanDocument
        fields = ('scan_type', 'scan_file', 'notes', 'report')
        widgets = {
            'scan_type': forms.Select(attrs={'class': 'form-control'}),
            'scan_file': forms.FileInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'report': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserUpdateForm(forms.ModelForm):
    """Update User Form"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class AppointmentCancellationForm(forms.Form):
    """Appointment Cancellation Form"""
    reason = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label='Cancellation Reason',
        required=False
    )


class PaymentForm(forms.Form):
    """Payment Form"""
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('BANK', 'Bank Transfer'),
        ('INSURANCE', 'Insurance'),
    ]
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        required=False,
        label='Additional Notes'
    )
