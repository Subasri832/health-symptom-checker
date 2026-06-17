from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SymptomCheck, ConversationMessage
from .ai_service import analyze_symptoms, get_severity_color, get_severity_emoji
from doctors.models import Doctor


def home(request):
    """Home page"""
    return render(request, 'home.html')


def symptom_checker(request):
    """Main symptom checker page"""
    return render(request, 'symptoms/checker.html')


@csrf_exempt
def analyze_symptoms_view(request):
    """API endpoint to analyze symptoms"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            symptoms_text = data.get("symptoms", "")
            language = data.get("language", "en")
            conversation_history = data.get("conversation_history", [])

            if not symptoms_text:
                return JsonResponse({"error": "No symptoms provided"}, status=400)

            # Get AI analysis
            result = analyze_symptoms(
                symptoms_text=symptoms_text,
                language=language,
                conversation_history=conversation_history
            )

            # Save to database
            symptom_check = SymptomCheck.objects.create(
                user=request.user if request.user.is_authenticated else None,
                symptoms_input=symptoms_text,
                language=language,
                ai_diagnosis=result["ai_diagnosis"],
                severity=result["severity"],
                recommended_speciality=result["recommended_speciality"],
                follow_up_questions=result["follow_up_questions"]
            )

            # Find nearby doctors based on speciality
            doctors = Doctor.objects.filter(
                speciality=result["recommended_speciality"],
                available=True
            )[:5]

            doctors_data = [{
                "id": d.id,
                "name": d.name,
                "speciality": d.get_speciality_display(),
                "hospital": d.hospital,
                "area": d.area,
                "city": d.city,
                "phone": d.phone,
                "rating": d.rating,
                "consultation_fee": d.consultation_fee,
                "latitude": d.latitude,
                "longitude": d.longitude,
            } for d in doctors]

            return JsonResponse({
                "success": True,
                "check_id": symptom_check.id,
                "diagnosis": result["ai_diagnosis"],
                "severity": result["severity"],
                "severity_color": get_severity_color(result["severity"]),
                "severity_emoji": get_severity_emoji(result["severity"]),
                "recommended_speciality": result["recommended_speciality"],
                "immediate_advice": result["immediate_advice"],
                "follow_up_questions": result["follow_up_questions"],
                "possible_conditions": result["possible_conditions"],
                "doctors": doctors_data,
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Method not allowed"}, status=405)


@login_required
def health_history(request):
    """Patient health history dashboard"""
    checks = SymptomCheck.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'symptoms/history.html', {'checks': checks})