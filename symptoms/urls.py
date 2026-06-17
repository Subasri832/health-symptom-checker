from django.urls import path
from . import views

urlpatterns = [
    path('', views.symptom_checker, name='symptom_checker'),
    path('analyze/', views.analyze_symptoms_view, name='analyze_symptoms'),
    path('history/', views.health_history, name='health_history'),
]