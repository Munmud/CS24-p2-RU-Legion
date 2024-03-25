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
    zone = models.IntegerField()
    ward = models.IntegerField()
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Sts in {self.address}"


class Landfill(models.Model):
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)


class WasteTransfer(models.Model):
    sts = models.ForeignKey(STS, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    departure = models.DateTimeField(null=True)
    arrival = models.DateTimeField(null=True)

    def __str__(self):
        return f"Transfer from {self.sts} departure at {self.departure}"


class WasteDumping(models.Model):
    landfill = models.ForeignKey(Landfill, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    departure = models.DateTimeField(null=True)
    arrival = models.DateTimeField(null=True)

    def __str__(self):
        return f"Transfer from {self.sts} departure at {self.departure}"
