from django.contrib import admin
from .models import (
    Department, Patient, Doctor, Room, Appointment, Prescription,
    RoomReservation, ContactInquiry, MedicalRecord, PaymentRecord, ScanDocument
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'department_code', 'chairman', 'location', 'contact_number')
    search_fields = ('name', 'department_code')
    readonly_fields = ('established_date',)


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'patient_number', 'phone', 'admission_date', 'blood_type')
    search_fields = ('user__first_name', 'user__last_name', 'patient_number', 'social_security_number')
    list_filter = ('blood_type', 'gender', 'admission_date')
    readonly_fields = ('admission_date',)
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Name'


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'license_number', 'specialty', 'department', 'consultation_fee', 'rating')
    search_fields = ('user__first_name', 'user__last_name', 'license_number')
    list_filter = ('specialty', 'department', 'join_date')
    readonly_fields = ('join_date', 'rating')
    
    def get_full_name(self, obj):
        return f"Dr. {obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Doctor Name'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'department', 'floor', 'beds_available', 'daily_rate', 'is_available')
    search_fields = ('room_number', 'room_type')
    list_filter = ('room_type', 'department', 'is_available', 'floor')
    list_editable = ('is_available', 'beds_available')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'patient', 'doctor', 'appointment_date', 'status', 'cost')
    search_fields = ('appointment_id', 'patient__user__first_name', 'doctor__user__first_name')
    list_filter = ('status', 'appointment_date', 'created_at')
    readonly_fields = ('appointment_id', 'created_at', 'updated_at')
    date_hierarchy = 'appointment_date'


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('medication_name', 'patient', 'doctor', 'start_date', 'end_date', 'frequency')
    search_fields = ('medication_name', 'patient__user__first_name', 'doctor__user__first_name')
    list_filter = ('start_date', 'end_date')
    readonly_fields = ('prescription_date',)
    date_hierarchy = 'prescription_date'


@admin.register(RoomReservation)
class RoomReservationAdmin(admin.ModelAdmin):
    list_display = ('patient', 'room', 'check_in_date', 'check_out_date', 'status', 'total_cost')
    search_fields = ('patient__user__first_name', 'room__room_number')
    list_filter = ('status', 'check_in_date')
    readonly_fields = ('created_at',)
    date_hierarchy = 'check_in_date'


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'is_responded', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_filter = ('inquiry_type', 'is_responded', 'created_at')
    readonly_fields = ('created_at',)
    list_editable = ('is_responded',)
    date_hierarchy = 'created_at'


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'record_date', 'blood_pressure', 'heart_rate', 'temperature', 'weight')
    search_fields = ('patient__user__first_name',)
    list_filter = ('record_date', 'recorded_by')
    readonly_fields = ('record_date',)
    date_hierarchy = 'record_date'


@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'payment_method', 'status', 'transaction_id', 'payment_date')
    search_fields = ('patient__user__first_name', 'transaction_id')
    list_filter = ('status', 'payment_method', 'payment_date')
    readonly_fields = ('payment_date',)
    date_hierarchy = 'payment_date'


@admin.register(ScanDocument)
class ScanDocumentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'scan_type', 'scan_date', 'uploaded_at')
    search_fields = ('patient__user__first_name', 'scan_type')
    list_filter = ('scan_type', 'scan_date')
    readonly_fields = ('scan_date', 'uploaded_at')
    date_hierarchy = 'scan_date'
