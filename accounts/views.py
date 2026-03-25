from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.user.is_authenticated:
        return redirect('generator:app_view')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('generator:app_view')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('generator:app_view')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already in use.')
        else:
            username = email.split('@')[0]
            # Handle duplicate usernames by appending logic if needed, but simple for now
            if User.objects.filter(username=username).exists():
                import time
                username = f"{username}{int(time.time())}"
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()
            login(request, user)
            return redirect('generator:app_view')

    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('generator:landing')
