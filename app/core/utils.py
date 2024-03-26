import os
import csv
from django.conf import settings
import re
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")
VEHICLE_METADATA_CSV = os.path.join(settings.DATA_DIR, "vehicle.csv")


def create_system_admin(username, email, password):
    if not User.objects.filter(username=username).exists():
        user = User.objects.create_user(
            username=username, password=password, email=email)
        group, created = Group.objects.get_or_create(name='System Admin')
        user.groups.add(group)
        user.is_staff = True
        user.save()
        print(f"User '{username}' is now a system admin.")


def is_system_admin(user):
    return user.groups.filter(name='System Admin').exists()


def load_sts():
    dataset = []
    with open(STS_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            data = {
                'ward':  int(row.get("ward")),
                'capacity':  int(row.get("capacity")),
                'zone':  int(row.get("zone")),
                'address': row.get("address"),
                'latitude':  row.get("latitude"),
                'longitude':  row.get("longitude"),
            }
            dataset.append(data)
    return dataset


def load_vehicle():
    dataset = []
    with open(VEHICLE_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            data = {
                'vehicle_number': row.get("vehicle_number"),
                'type': row.get("type"),
                'capacity': int(row.get("capacity")),
                'loaded_fuel_cost_per_km':  float(row.get("loaded_fuel_cost_per_km")),
                'unloaded_fuel_cost_per_km': float(row.get("unloaded_fuel_cost_per_km"))
            }
            dataset.append(data)
            # print(data)
            # break
    return dataset
