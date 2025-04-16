from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Bike(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_year = models.IntegerField()
    engine_capacity = models.CharField(max_length=20)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    real_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 💰 Real value of the bike
    image = models.ImageField(upload_to='bike_images/')
    description = models.TextField()

    def is_available_for_dates(self, start_date, end_date):
        # Check if there are any overlapping bookings for the bike within the given date range
        bookings = self.booking_set.filter(
            rent_start_date__lte=end_date,
            rent_end_date__gte=start_date
        )
        return not bookings.exists()

    def get_booked_dates(self):
        # Get all the booked dates for the bike
        bookings = Booking.objects.filter(bike=self)
        booked_dates = []
        for booking in bookings:
            booked_dates.append({
                'start_date': booking.rent_start_date,
                'end_date': booking.rent_end_date
            })
        return booked_dates

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    # Customer details
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    adhar = models.CharField(max_length=12)
    license_number = models.CharField(max_length=20)
    license_image = models.ImageField(upload_to='license_images/')
    
    # Payment-related fields
    payment_method = models.CharField(
        max_length=20,
        choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card')],
        default='Cash'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid')],
        default='Pending'
    )
    total_rent = models.DecimalField(max_digits=10, decimal_places=2)
    security_deposit = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_total_rent(self):
        # Calculate the total rent based on the rental period and the bike's price per day
        num_days = (self.rent_end_date - self.rent_start_date).days + 1
        rent = self.bike.price_per_day * Decimal(num_days)
        self.total_rent = rent
        self.security_deposit = rent * Decimal('0.07')  # 7% security deposit
        return rent + self.security_deposit

    def __str__(self):
        return f"Booking for {self.bike.name} by {self.user.username}"
