from django.contrib import admin
from .models import Doctor, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'speciality', 'hospital', 'city', 'rating', 'available']
    list_filter = ['speciality', 'city', 'available']
    search_fields = ['name', 'hospital', 'city']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'doctor', 'appointment_date', 'status']
    list_filter = ['status', 'appointment_date']