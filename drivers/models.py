from django.db import models
from django.core.validators import RegexValidator


class Driver(models.Model):
    """
    Model representing a driver in the ride-hailing system.
    """
    
    VEHICLE_TYPE_CHOICES = [
        ('Bike', 'Bike'),
        ('Auto', 'Auto'),
        ('Hatchback', 'Hatchback'),
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
    ]
    
    driver_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, help_text="Driver's full name")
    
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits"
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=10,
        unique=True,
        help_text="10-digit phone number"
    )
    
    vehicle_type = models.CharField(
        max_length=20,
        choices=VEHICLE_TYPE_CHOICES,
        help_text="Type of vehicle"
    )
    
    vehicle_plate = models.CharField(
        max_length=20,
        unique=True,
        help_text="Vehicle registration plate number"
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the driver is currently active"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'drivers'
        ordering = ['-driver_id']
        indexes = [
            models.Index(fields=['is_active']),
            models.Index(fields=['vehicle_type']),
            models.Index(fields=['phone']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.vehicle_type} - {self.vehicle_plate})"

