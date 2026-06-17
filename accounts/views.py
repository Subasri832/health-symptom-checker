from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages


def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        login(request, user)
        messages.success(request, f"Welcome {username}! Account created successfully.")
        return redirect('home')

    return render(request, 'accounts/register.html')