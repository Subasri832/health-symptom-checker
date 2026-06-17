from django.shortcuts import render
from django.http import JsonResponse
from .models import Doctor


def doctor_list(request):
    """All doctors page"""
    speciality = request.GET.get('speciality', '')
    city = request.GET.get('city', '')

    doctors = Doctor.objects.filter(available=True)

    if speciality:
        doctors = doctors.filter(speciality=speciality)
    if city:
        doctors = doctors.filter(city__icontains=city)

    specialities = Doctor.SPECIALITY_CHOICES

    return render(request, 'doctors/list.html', {
        'doctors': doctors,
        'specialities': specialities,
        'selected_speciality': speciality,
        'selected_city': city,
    })


def doctor_map(request):
    """Doctor map view — returns JSON for map"""
    speciality = request.GET.get('speciality', '')
    doctors = Doctor.objects.filter(available=True)

    if speciality:
        doctors = doctors.filter(speciality=speciality)

    data = [{
        'id': d.id,
        'name': f"Dr. {d.name}",
        'speciality': d.get_speciality_display(),
        'hospital': d.hospital,
        'area': d.area,
        'city': d.city,
        'phone': d.phone,
        'rating': d.rating,
        'fee': d.consultation_fee,
        'lat': d.latitude,
        'lng': d.longitude,
    } for d in doctors]

    return JsonResponse({'doctors': data})