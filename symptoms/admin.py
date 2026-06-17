from django.contrib import admin
from .models import SymptomCheck, ConversationMessage


@admin.register(SymptomCheck)
class SymptomCheckAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'severity', 'recommended_speciality', 'language', 'created_at']
    list_filter = ['severity', 'language', 'created_at']
    search_fields = ['symptoms_input', 'ai_diagnosis']
    readonly_fields = ['created_at']


@admin.register(ConversationMessage)
class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'symptom_check', 'role', 'created_at']
    list_filter = ['role']