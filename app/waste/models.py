from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.conf import settings


VEHICLE_TYPES = [
    ('Open Truck', 'Open Truck'),
    ('Dump Truck', 'Dump Truck'),
    ('Compactor', 'Compactor'),
    ('Container Carrier', 'Container Carrier'),
]

CAPACITY_CHOICES = [
    (1, '1 ton'),
    (2, '2 ton'),
    (3, '3 ton'),
    (4, '4 ton'),
    (5, '5 ton'),
    (6, '6 ton'),
    (7, '7 ton'),
    (8, '8 ton'),
    (9, '9 ton'),
    (10, '10 ton'),
]

VEHICLE_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Inactive', 'Inactive'),
    ('Under Maintenance', 'Under Maintenance'),
    ('In Transit', 'In Transit'),
]


class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.IntegerField(choices=CAPACITY_CHOICES)
    loaded_fuel_cost_per_km = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0)
    unloaded_fuel_cost_per_km = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0)
    status = models.CharField(
        max_length=20, choices=VEHICLE_STATUS_CHOICES, default='Available')

    def __str__(self):
        return f"{self.capacity} tons {self.type} {self.vehicle_number}"


class STS(models.Model):
    zone = models.IntegerField()
    ward = models.IntegerField()
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    def __str__(self):
        return f"Sts in {self.address}"


class STSManager(models.Model):
    sts = models.ForeignKey(STS, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user']


@receiver(models.signals.post_save, sender=STSManager)
def create_sts_manager(sender, instance, created, **kwargs):
    if created:
        group, create = Group.objects.get_or_create(
            name=settings.GROUP_NAME_STS_MANAGER)
        user = User.objects.get(username=instance.user.username)
        user.groups.add(group)


@receiver(models.signals.post_delete, sender=STSManager)
def delete_sts_manager(sender, instance, **kwargs):
    group, created = Group.objects.get_or_create(
        name=settings.GROUP_NAME_STS_MANAGER)
    user = User.objects.get(username=instance.user.username)
    user.groups.remove(group)


class Landfill(models.Model):
    address = models.CharField(max_length=255)
    capacity = models.IntegerField()
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)

    def __str__(self):
        return f"Landfill in {self.address}"


class LandfillManager(models.Model):
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user']


@receiver(models.signals.post_save, sender=LandfillManager)
def create_landfill_manager(sender, instance, created, **kwargs):
    if created:
        group, create = Group.objects.get_or_create(
            name=settings.GROUP_NAME_LANDFILL_MANAGER)
        user = User.objects.get(username=instance.user.username)
        user.groups.add(group)


@receiver(models.signals.post_delete, sender=LandfillManager)
def delete_landfill_manager(sender, instance, **kwargs):
    group, created = Group.objects.get_or_create(
        name=settings.GROUP_NAME_LANDFILL_MANAGER)
    user = User.objects.get(username=instance.user.username)
    user.groups.remove(group)


class WasteTransfer(models.Model):
    sts = models.ForeignKey(STS, on_delete=models.DO_NOTHING)
    landfill = models.ForeignKey(Landfill, on_delete=models.DO_NOTHING)
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
