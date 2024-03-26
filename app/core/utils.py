import os
import csv
from django.conf import settings
import re


STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")
VEHICLE_METADATA_CSV = os.path.join(settings.DATA_DIR, "vehicle.csv")


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
