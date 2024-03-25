from django.db import models
from django.contrib.auth.models import User

VEHICLE_TYPES = [
    ('Open Truck', 'Open Truck'),
    ('Dump Truck', 'Dump Truck'),
    ('Compactor', 'Compactor'),
    ('Container Carrier', 'Container Carrier'),
]
CAPACITY_CHOICES = [
    (3, '3 ton'),
    (5, '5 ton'),
    (7, '7 ton'),
]


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)

    def __str__(self):
        return f"{self.vehicle_number} {self.type} {self.capacity}"


class STS(models.Model):
    Zone = models.IntegerField()
    Ward = models.IntegerField()
    Address = models.CharField(max_length=255)
    Capacity = models.IntegerField()
    Latitude = models.DecimalField(max_digits=9, decimal_places=6)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6)
    STS_Manager_ID = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Sts in {self.Address}"
