from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.conf import settings
from celery import shared_task
from django.shortcuts import get_object_or_404
from django.db import transaction

from core.utils import aws_map_route_api
import json


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
    (11, '11 ton'),
    (12, '12 ton'),
    (13, '13 ton'),
    (14, '14 ton'),
    (15, '15 ton'),
]

VEHICLE_STATUS_CHOICES = [
    ('Available', 'Available'),
    ('Inactive', 'Inactive'),
    ('Under Maintenance', 'Under Maintenance'),
    ('In Transit', 'In Transit'),
]

WASTE_TRANSFER_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Sending to Landfill', 'Sending to Landfill'),
    ('Dumping in Landfill', 'Dumping in Landfill'),
    ('Returning to STS', 'Returning to STS'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
]

PATH_OPTIMIZE_CHOICES = (
    ('FastestRoute', 'FastestRoute'),
    ('ShortestRoute', 'ShortestRoute'),
)

WASTE_TRANSFER_QUEUE_STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Completed', 'Completed'),
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
        return f"{self.address}"

    class Meta:
        unique_together = ['latitude', 'longitude']


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
        return f"{self.address}"

    class Meta:
        unique_together = ['latitude', 'longitude']


@shared_task
def add_to_path(sts_id, landfill_id):
    with transaction.atomic():
        sts = get_object_or_404(STS, id=sts_id)
        landfill = get_object_or_404(Landfill, id=landfill_id)
        OptimizeForList = ['FastestRoute', 'ShortestRoute']
        for OptimizeFor in OptimizeForList:
            if Path.objects.filter(
                sts=sts,
                landfill=landfill,
                OptimizeFor=OptimizeFor
            ).exists():
                return
            res = aws_map_route_api(
                source_lat=sts.latitude,
                source_lon=sts.longitude,
                dest_lat=landfill.latitude,
                dest_lon=landfill.longitude,
                OptimizeFor=OptimizeFor
            )
            DriveDistance = res['DriveDistance']
            DistanceUnit = res['DistanceUnit']
            DriveTime = res['DriveTime']
            TimeUnit = res['TimeUnit']
            PathList = json.dumps({"PathList": res['PathList']})
            path, created = Path.objects.get_or_create(
                sts=sts,
                landfill=landfill,
                OptimizeFor=OptimizeFor,
                DriveDistance=DriveDistance,
                DistanceUnit=DistanceUnit,
                DriveTime=DriveTime,
                TimeUnit=TimeUnit,
                points=PathList
            )


@receiver(models.signals.post_save, sender=STS)
def create_sts(sender, instance, created, **kwargs):
    if created:
        for landfill in Landfill.objects.all():
            add_to_path.apply_async(
                args=[instance.id, landfill.id], countdown=10)


@receiver(models.signals.post_save, sender=Landfill)
def create_Landfill(sender, instance, created, **kwargs):
    if created:
        for sts in STS.objects.all():
            add_to_path.apply_async(
                args=[sts.id, instance.id], countdown=10)


class LandfillManager(models.Model):
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user']


class Path(models.Model):
    sts = models.ForeignKey(STS, on_delete=models.CASCADE)
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE)
    points = models.TextField()
    OptimizeFor = models.CharField(
        max_length=20, choices=PATH_OPTIMIZE_CHOICES)
    AvoidTolls = models.BooleanField(default=False)
    DriveDistance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    DistanceUnit = models.CharField(max_length=20, null=True, blank=True)
    DriveTime = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    TimeUnit = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.OptimizeFor} {self.DriveDistance}km {self.DriveTime} minute"

    class Meta:
        unique_together = ['sts', 'landfill', 'OptimizeFor', 'AvoidTolls']


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
    departure_from_sts = models.DateTimeField(null=True)
    departure_from_landfill = models.DateTimeField(null=True)
    arrival_at_landfill = models.DateTimeField(null=True)
    arrival_at_sts = models.DateTimeField(null=True)
    status = models.CharField(
        max_length=20,
        choices=WASTE_TRANSFER_STATUS_CHOICES,
        default='Pending'
    )
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    arrival_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    return_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)
    total_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Transfer from {self.sts} departure at {self.departure_from_sts}"


def calculate_fuel_cost(transfer_id):
    fuel_cost_per_litre = settings.FUEL_COST_PER_LITRE
    transfer = get_object_or_404(WasteTransfer, id=transfer_id)
    carried_volume = transfer.volume

    path = transfer.path
    distance = path.DriveDistance

    vehicle = transfer.vehicle
    loaded_cost = vehicle.loaded_fuel_cost_per_km
    unloaded_cost = vehicle.unloaded_fuel_cost_per_km
    vehicle_capacity = vehicle.capacity

    cost_driving_unloaded = (unloaded_cost*distance*fuel_cost_per_litre)
    cost_driving_loaded = (loaded_cost*distance*fuel_cost_per_litre)

    arrival_cost = cost_driving_unloaded + \
        (cost_driving_loaded-cost_driving_unloaded) * \
        (carried_volume/vehicle_capacity)
    return arrival_cost, cost_driving_unloaded


@shared_task
def add_transfer_cost(transfer_id):
    arrival_cost, return_cost = calculate_fuel_cost(transfer_id)
    transfer = get_object_or_404(WasteTransfer, id=transfer_id)
    transfer.arrival_cost = arrival_cost
    transfer.return_cost = return_cost
    transfer.total_cost = arrival_cost+return_cost
    transfer.save()


@receiver(models.signals.post_save, sender=WasteTransfer)
def update_vehicle_status(sender, instance, created, **kwargs):
    if instance.status not in ['Completed', 'Cancelled']:
        instance.vehicle.status = 'In Transit'
        instance.vehicle.save()
    else:
        instance.vehicle.status = 'Available'
        instance.vehicle.save()
    if created:
        add_transfer_cost.delay(instance.id)


class WasteTransferQueue(models.Model):
    sts = models.ForeignKey(STS, on_delete=models.CASCADE)
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    path = models.ForeignKey(Path, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=WASTE_TRANSFER_QUEUE_STATUS_CHOICES,
        default='Pending'
    )
