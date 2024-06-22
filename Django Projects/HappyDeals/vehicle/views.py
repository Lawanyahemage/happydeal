# vehicle/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Vehicle
from .forms import VehicleForm
from .models import  Booking
from datetime import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, LoginForm

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('vehicle_list')  # Redirect to the admin interface
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'vehicle/login.html', {'form': form})

def home(request):
    vehicles = Vehicle.objects.all()  # Retrieve all vehicle objects
    return render(request, 'home.html', {'vehicles': vehicles})

def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    return render(request, 'vehicle/vehicle_list.html', {'vehicles': vehicles})

def vehicle_add(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicle/vehicle_form.html', {'form': form})

def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicle/vehicle_form.html', {'form': form})

def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')
    return render(request, 'vehicle/vehicle_confirm_delete.html', {'vehicle': vehicle})


def rent_vehicle(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)

    if request.method == 'POST':
        customer_name = request.POST.get('customerName')
        customer_phone = request.POST.get('customerPhone')
        pickup_date = datetime.strptime(request.POST.get('pickupDate'), '%Y-%m-%d').date()
        return_date = datetime.strptime(request.POST.get('returnDate'), '%Y-%m-%d').date()

        try:
            new_booking = Booking(vehicle=vehicle, customer=request.user, pickup_date=pickup_date,
                                  return_date=return_date)
            new_booking.save()
            messages.success(request, f"Booking successful for {vehicle.name} from {pickup_date} to {return_date}.")

        except ValueError as e:
            messages.error(request, str(e))  # Display error message if booking overlaps

    return render(request, 'vehicle/rent_form.html', {'vehicle': vehicle})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('customer_login')
    else:
        form = UserRegistrationForm()
    return render(request, 'user/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with your actual home URL name
    else:
        form = LoginForm()
    return render(request, 'user/customer.html', {'form': form})