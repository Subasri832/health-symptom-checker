from django.db import models
from django.contrib.auth.models import User


class SymptomCheck(models.Model):
    SEVERITY_CHOICES = [
        ('mild', 'Mild'),
        ('moderate', 'Moderate'),
        ('serious', 'Serious'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('ta', 'Tamil'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    symptoms_input = models.TextField()
    language = models.CharField(
        max_length=5,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    ai_diagnosis = models.TextField()
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default='mild'
    )
    recommended_speciality = models.CharField(
        max_length=100,
        blank=True
    )
    follow_up_questions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check #{self.id} - {self.severity} - {self.created_at.date()}"

    class Meta:
        ordering = ['-created_at']


class ConversationMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    symptom_check = models.ForeignKey(
        SymptomCheck,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"

    class Meta:
        ordering = ['created_at']