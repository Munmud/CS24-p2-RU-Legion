import os
import csv
from django.conf import settings
import re

STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")


def is_system_admin(user):
    return user.groups.filter(name='System Admin').exists()


def load_sts():
    dataset = []
    # Regular expression pattern to extract latitude and longitude
    pattern = r'(\d+\.\d+)°\s*([NS]),\s*(\d+\.\d+)°\s*([EW])'
    with open(STS_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            try:
                Ward = int(row.get("Ward"))
                Zone = int(row.get("Zone"))
                Capacity = int(row.get("Capacity"))
                Address = row.get("Address")
                match = re.match(pattern, row.get("GPS Location"))
                if match:
                    Latitude = float(match.group(1))
                    if match.group(2) == 'S':
                        Latitude *= -1  # Southern hemisphere
                    Longitude = float(match.group(3))
                    if match.group(4) == 'W':
                        Longitude *= -1  # Western hemisphere
            except Exception as e:
                continue
            data = {
                'Ward':  Ward,
                'Capacity':  Capacity,
                'Zone':  Zone,
                'Address':  Address,
                'Latitude':  Latitude,
                'Longitude':  Longitude,
            }
            dataset.append(data)
    return dataset
