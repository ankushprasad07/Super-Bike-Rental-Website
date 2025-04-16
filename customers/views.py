from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.serializers import serialize


def register_customer(request):
    if request.method == 'POST':
        user_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('customer_login')
    else:
        user_form = CustomerRegistrationForm()
    return render(request, 'customers/register.html', {
        'user_form': user_form,
    })


def login_customer(request):
    if request.method == 'POST':
        form = CustomerLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_staff:  # Only allow customers (not superuser/staff)
                    login(request, user)
                    return redirect('bike_list')  # Change this later to the homepage
                else:
                    messages.error(request, 'Superuser/staff cannot log in here.')
            else:
                messages.error(request, 'Invalid credentials.')
    else:
        form = CustomerLoginForm()
    return render(request, 'customers/login.html', {'form': form})

def logout_customer(request):
    logout(request)
    return redirect('customer_login')


def bike_list(request):
    bikes = Bike.objects.all()
    return render(request, 'customers/bike_list.html', {'bikes': bikes})


def bike_detail(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)
    
    # Get the booked dates for this bike
    booked_dates = Booking.objects.filter(bike=bike).values('rent_start_date', 'rent_end_date')
    
    context = {
        'bike': bike,
        'booked_dates': list(booked_dates),  # Convert to list for easy use in template
    }

    return render(request, 'customers/bike_detail.html', context)



@login_required
def booking_form(request, bike_id):
    bike = get_object_or_404(Bike, id=bike_id)

    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        adhar = request.POST['adhar']
        license_number = request.POST['license_number']
        license_image = request.FILES['license_image']
        rent_start_date = datetime.strptime(request.POST['rent_start_date'], '%Y-%m-%d').date()
        rent_end_date = datetime.strptime(request.POST['rent_end_date'], '%Y-%m-%d').date()

        # Check for overlapping booking
        if not bike.is_available_for_dates(rent_start_date, rent_end_date):
            return render(request, 'customers/booking_form.html', {
                'bike': bike,
                'error': 'This bike is already booked for the selected dates. Please choose different dates.'
            })

        # Create booking if available
        booking = Booking(
            bike=bike,
            user=request.user,
            name=name,
            phone=phone,
            adhar=adhar,
            license_number=license_number,
            license_image=license_image,
            rent_start_date=rent_start_date,
            rent_end_date=rent_end_date
        )
        booking.calculate_total_rent()
        booking.save()

        return redirect('payment', booking.id)

    return render(request, 'customers/booking_form.html', {'bike': bike})



def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        method = request.POST.get('payment_method')
        if method == 'cash':
            booking.payment_method = 'Cash'
            booking.payment_status = 'Pending'
        else:
            booking.payment_method = 'Credit Card'
            booking.payment_status = 'Paid'

        booking.save()
        return redirect('customer_dashboard')

    return render(request, 'customers/payment.html', {'booking': booking})



@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-id')
    return render(request, 'customers/dashboard.html', {'bookings': bookings})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'pending':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.warning(request, "Only pending bookings can be cancelled.")
    return redirect('customer_dashboard')


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if booking.status == 'cancelled':
        booking.delete()
        messages.success(request, "Booking deleted successfully.")
    else:
        messages.warning(request, "You can only delete cancelled bookings.")
    return redirect('customer_dashboard')