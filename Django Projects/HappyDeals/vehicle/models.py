from django.db import models
from django.contrib.auth.models import User


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=50)
    max_persons = models.IntegerField()
    fuel_efficiency = models.FloatField()
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image_url = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class Booking(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    pickup_date = models.DateField()
    return_date = models.DateField()

    def __str__(self):
        return f"{self.vehicle.name} - {self.pickup_date} to {self.return_date}"

    def save(self, *args, **kwargs):
        # Check for overlapping bookings
        overlapping_bookings = Booking.objects.filter(vehicle=self.vehicle).filter(
            models.Q(pickup_date__range=[self.pickup_date, self.return_date]) |
            models.Q(return_date__range=[self.pickup_date, self.return_date])
        ).exclude(pk=self.pk)  # Exclude current booking if updating
        if overlapping_bookings.exists():
            raise ValueError("This vehicle is already booked for the given dates.")

        super().save(*args, **kwargs)


