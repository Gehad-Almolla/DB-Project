from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

class Department(models.Model):
    """Surgery Department Model"""
    department_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    chairman = models.OneToOneField('Doctor', on_delete=models.SET_NULL, null=True, related_name='chaired_department')
    established_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'departments'
    
    def __str__(self):
        return f"{self.name} ({self.department_code})"


class Patient(models.Model):
    """Patient Model"""
    BLOOD_TYPES = [
        ('O+', 'O+'), ('O-', 'O-'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]
    
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    patient_number = models.CharField(max_length=50, unique=True)
    social_security_number = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    medical_history = models.TextField(blank=True, null=True)
    admission_date = models.DateField(default=timezone.now)
    emergency_contact = models.CharField(max_length=100)
    emergency_phone = models.CharField(max_length=20)
    profile_photo = models.ImageField(upload_to='patient_photos/', blank=True, null=True)
    
    class Meta:
        db_table = 'patients'
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.patient_number})"


class MedicalRecord(models.Model):
    """Patient Medical Status"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    record_date = models.DateTimeField(auto_now_add=True)
    blood_pressure = models.CharField(max_length=20)  # e.g., "120/80"
    heart_rate = models.IntegerField(validators=[MinValueValidator(40), MaxValueValidator(200)])
    temperature = models.FloatField(validators=[MinValueValidator(35), MaxValueValidator(42)])
    weight = models.FloatField(validators=[MinValueValidator(20), MaxValueValidator(300)])
    height = models.FloatField(validators=[MinValueValidator(100), MaxValueValidator(230)])
    notes = models.TextField(blank=True)
    recorded_by = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'medical_records'
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.patient} - {self.record_date}"


class Doctor(models.Model):
    """Doctor Model"""
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    SPECIALTIES = [
        ('SURGERY', 'General Surgery'),
        ('ORTHOPEDIC', 'Orthopedic Surgery'),
        ('CARDIO_SURGERY', 'Cardiac Surgery'),
        ('NEURO_SURGERY', 'Neurosurgery'),
        ('VASCULAR_SURGERY', 'Vascular Surgery'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    license_number = models.CharField(max_length=50, unique=True)
    social_security_number = models.CharField(max_length=20, unique=True)
    birthdate = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    specialty = models.CharField(max_length=50, choices=SPECIALTIES)
    degree = models.CharField(max_length=100)  # e.g., "MD", "PhD", "Board Certified"
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')
    join_date = models.DateField(default=timezone.now)
    qualification_document = models.FileField(upload_to='doctor_qualifications/', blank=True, null=True)
    profile_photo = models.ImageField(upload_to='doctor_photos/', blank=True, null=True)
    office_location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    rating = models.FloatField(default=5.0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    
    class Meta:
        db_table = 'doctors'
    
    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Room(models.Model):
    """Hospital Room Model"""
    ROOM_TYPES = [
        ('GENERAL', 'General Ward'),
        ('SEMI_PRIVATE', 'Semi-Private'),
        ('PRIVATE', 'Private'),
        ('ICU', 'ICU'),
        ('OPERATION', 'Operation Theatre'),
    ]
    
    room_number = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='rooms')
    floor = models.IntegerField()
    beds_total = models.IntegerField(validators=[MinValueValidator(1)])
    beds_available = models.IntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)
    equipment = models.TextField(blank=True)  # List of equipment
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        db_table = 'rooms'
    
    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"


class Appointment(models.Model):
    """Appointment between Doctor and Patient"""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('CONFIRMED', 'Confirmed'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('NO_SHOW', 'No Show'),
    ]
    
    appointment_id = models.UUIDField(default=uuid.uuid4, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    duration_minutes = models.IntegerField(default=30, validators=[MinValueValidator(15), MaxValueValidator(180)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SCHEDULED')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_date']
    
    def __str__(self):
        return f"{self.patient} - Dr. {self.doctor.user.first_name} ({self.appointment_date})"


class Prescription(models.Model):
    """Prescription Model"""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)  # e.g., "500mg"
    frequency = models.CharField(max_length=100)  # e.g., "2 times daily"
    start_date = models.DateField()
    end_date = models.DateField()
    instructions = models.TextField()
    prescription_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    refills_remaining = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'prescriptions'
        ordering = ['-prescription_date']
    
    def __str__(self):
        return f"{self.medication_name} - {self.patient}"


class RoomReservation(models.Model):
    """Room Reservation Model"""
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('OCCUPIED', 'Occupied'),
        ('DISCHARGED', 'Discharged'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='room_reservations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    check_in_date = models.DateTimeField()
    check_out_date = models.DateTimeField(null=True, blank=True)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'room_reservations'
    
    def __str__(self):
        return f"{self.patient} - Room {self.room.room_number} ({self.status})"


class ContactInquiry(models.Model):
    """Contact Form Inquiries"""
    INQUIRY_TYPES = [
        ('APPOINTMENT', 'Appointment Inquiry'),
        ('GENERAL', 'General Inquiry'),
        ('COMPLAINT', 'Complaint'),
        ('FEEDBACK', 'Feedback'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    message = models.TextField()
    attachment = models.FileField(upload_to='inquiries/', blank=True, null=True)
    is_responded = models.BooleanField(default=False)
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'contact_inquiries'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.inquiry_type}"


class PaymentRecord(models.Model):
    """Payment Record Model"""
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    ]
    
    PAYMENT_METHOD = [
        ('CASH', 'Cash'),
        ('CARD', 'Credit/Debit Card'),
        ('BANK', 'Bank Transfer'),
        ('INSURANCE', 'Insurance'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    room_reservation = models.ForeignKey(RoomReservation, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'payment_records'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.patient} - ${self.amount} ({self.status})"


class ScanDocument(models.Model):
    """Patient Scan Documents (X-Ray, MRI, CT, etc.)"""
    SCAN_TYPES = [
        ('XRAY', 'X-Ray'),
        ('MRI', 'MRI Scan'),
        ('CT', 'CT Scan'),
        ('ULTRASOUND', 'Ultrasound'),
        ('PATHOLOGY', 'Pathology Report'),
        ('OTHER', 'Other'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='scans')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    scan_type = models.CharField(max_length=20, choices=SCAN_TYPES)
    scan_file = models.FileField(upload_to='patient_scans/')
    scan_date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)
    report = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'scan_documents'
        ordering = ['-scan_date']
    
    def __str__(self):
        return f"{self.patient} - {self.get_scan_type_display()}"
