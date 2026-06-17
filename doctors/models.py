from django.db import models


class Doctor(models.Model):
    SPECIALITY_CHOICES = [
        ('general', 'General Physician'),
        ('cardiologist', 'Cardiologist'),
        ('dermatologist', 'Dermatologist'),
        ('neurologist', 'Neurologist'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrician', 'Pediatrician'),
        ('psychiatrist', 'Psychiatrist'),
        ('gynecologist', 'Gynecologist'),
        ('ent', 'ENT Specialist'),
        ('ophthalmologist', 'Ophthalmologist'),
        ('gastroenterologist', 'Gastroenterologist'),
        ('pulmonologist', 'Pulmonologist'),
        ('endocrinologist', 'Endocrinologist'),
        ('urologist', 'Urologist'),
        ('oncologist', 'Oncologist'),
    ]

    name = models.CharField(max_length=200)
    speciality = models.CharField(
        max_length=50,
        choices=SPECIALITY_CHOICES
    )
    hospital = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    rating = models.FloatField(default=4.0)
    available = models.BooleanField(default=True)
    consultation_fee = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Dr. {self.name} - {self.speciality}"

    class Meta:
        ordering = ['-rating']


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    patient_name = models.CharField(max_length=200)
    patient_phone = models.CharField(max_length=15)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient_name} - Dr.{self.doctor.name} - {self.appointment_date}"

    class Meta:
        ordering = ['-created_at']