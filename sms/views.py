from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Trip, Request

def home(request):
    trips = Trip.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'trips': trips})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        
        if not username or not email or not password:
            messages.error(request, 'All fields are required')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'register.html')
            
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
        except:
            messages.error(request, 'Error creating account')
            return render(request, 'register.html')
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        if not username or not password:
            messages.error(request, 'Both username and password are required')
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong username or password')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')