from django.contrib import admin
from django.urls import path, include
from symptoms.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('symptoms/', include('symptoms.urls')),
    path('doctors/', include('doctors.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]