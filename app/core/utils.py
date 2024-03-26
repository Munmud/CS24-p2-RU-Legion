import os
import csv
from django.conf import settings
import re
from django.core.mail import send_mail

STS_METADATA_CSV = os.path.join(settings.DATA_DIR, "sts.csv")
VEHICLE_METADATA_CSV = os.path.join(settings.DATA_DIR, "vehicle.csv")


def is_system_admin(user):
    return user.groups.filter(name='System Admin').exists()


def send_forget_password_mail(email, token):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password http://127.0.0.1:8000/auth/change-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    # send_mail(subject, message, email_from, recipient_list)
    send_mail(subject, message, email_from, recipient_list)

    return True


def load_sts():
    dataset = []
    # Regular expression pattern to extract latitude and longitude
    pattern = r'(\d+\.\d+)°\s*([NS]),\s*(\d+\.\d+)°\s*([EW])'
    with open(STS_METADATA_CSV, newline='', encoding="utf8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # print(row)
            try:
                ward = int(row.get("ward"))
                zone = int(row.get("zone"))
                capacity = int(row.get("capacity"))
                address = row.get("address")
                match = re.match(pattern, row.get("gps"))
                if match:
                    latitude = float(match.group(1))
                    if match.group(2) == 'S':
                        latitude *= -1  # Southern hemisphere
                    longitude = float(match.group(3))
                    if match.group(4) == 'W':
                        longitude *= -1  # Western hemisphere
            except Exception as e:
                print(e)
                continue
            data = {
                'ward':  ward,
                'capacity':  capacity,
                'zone':  zone,
                'address':  address,
                'latitude':  latitude,
                'longitude':  longitude,
            }
            dataset.append(data)
            # print(data)
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
            }
            dataset.append(data)
            # print(data)
            # break
    return dataset
