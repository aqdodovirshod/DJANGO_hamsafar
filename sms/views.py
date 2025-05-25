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

@login_required
def create_trip(request):
    if request.method == 'POST':
        start_location = request.POST.get('start_location', '')
        end_location = request.POST.get('end_location', '')
        date = request.POST.get('date', '')
        seats = request.POST.get('seats', '')
        description = request.POST.get('description', '')
        
        if not all([start_location, end_location, date, seats, description]):
            messages.error(request, 'All fields are required')
            return render(request, 'create_trip.html')
            
        try:
            seats = int(seats)
            if seats < 1:
                messages.error(request, 'Seats must be a positive number')
                return render(request, 'create_trip.html')
        except ValueError:
            messages.error(request, 'Seats must be a number')
            return render(request, 'create_trip.html')
            
        try:
            # Convert the datetime string to a timezone-aware datetime
            date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            
            trip = Trip(
                user=request.user,
                start_location=start_location,
                end_location=end_location,
                date=date,
                seats=seats,
                description=description
            )
            trip.save()
            messages.success(request, 'Trip created successfully')
            return redirect('home')
        except:
            messages.error(request, 'Error creating trip')
            return render(request, 'create_trip.html')

    return render(request, 'create_trip.html')

def search_trips(request):
    start = request.GET.get('start', '')
    end = request.GET.get('end', '')
    
    trips = Trip.objects.all().order_by('-created_at')
    
    if start:
        trips = trips.filter(start_location__icontains=start)
    if end:
        trips = trips.filter(end_location__icontains=end)
        
    return render(request, 'search_trips.html', {
        'trips': trips,
        'start': start,
        'end': end
    })

@login_required
def my_trips(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_trips.html', {'trips': trips})

@login_required
def delete_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    try:
        trip.delete()
        messages.success(request, 'Trip deleted successfully')
    except:
        messages.error(request, 'Error deleting trip')
    return redirect('my_trips')

@login_required
def edit_trip(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, user=request.user)
    
    if request.method == 'POST':
        start_location = request.POST.get('start_location', '')
        end_location = request.POST.get('end_location', '')
        date = request.POST.get('date', '')
        seats = request.POST.get('seats', '')
        description = request.POST.get('description', '')
        
        if not all([start_location, end_location, date, seats, description]):
            messages.error(request, 'All fields are required')
            return render(request, 'edit_trip.html', {'trip': trip})
            
        try:
            seats = int(seats)
            if seats < 1:
                messages.error(request, 'Seats must be a positive number')
                return render(request, 'edit_trip.html', {'trip': trip})
        except ValueError:
            messages.error(request, 'Seats must be a number')
            return render(request, 'edit_trip.html', {'trip': trip})
            
        try:
            # Convert the datetime string to a timezone-aware datetime
            date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            
            trip.start_location = start_location
            trip.end_location = end_location
            trip.date = date
            trip.seats = seats
            trip.description = description
            trip.save()
            messages.success(request, 'Trip updated successfully')
            return redirect('my_trips')
        except:
            messages.error(request, 'Error updating trip')
            return render(request, 'edit_trip.html', {'trip': trip})
            
    return render(request, 'edit_trip.html', {'trip': trip})

@login_required
def create_request(request):
    if request.method == 'POST':
        start_location = request.POST.get('start_location', '')
        end_location = request.POST.get('end_location', '')
        date = request.POST.get('date', '')
        message = request.POST.get('message', '')
        
        if not all([start_location, end_location, date, message]):
            messages.error(request, 'All fields are required')
            return render(request, 'create_request.html')
            
        try:
            # Convert the datetime string to a timezone-aware datetime
            date = timezone.make_aware(timezone.datetime.strptime(date, '%Y-%m-%dT%H:%M'))
            
            new_request = Request(
                user=request.user,
                start_location=start_location,
                end_location=end_location,
                date=date,
                message=message
            )
            new_request.save()
            messages.success(request, 'Request created successfully')
            return redirect('home')
        except:
            messages.error(request, 'Error creating request')
            return render(request, 'create_request.html')
        
    return render(request, 'create_request.html')
