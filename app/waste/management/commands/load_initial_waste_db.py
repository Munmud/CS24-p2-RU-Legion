import os
import random
# from tqdm import tqdm
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from core.utils import load_sts, load_vehicle
from waste.models import STS, Vehicle, Landfill


class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        for sts in load_sts():
            STS.objects.create(**sts)
        print('Successfully loaded sts db...')

        for vehicle in load_vehicle():
            Vehicle.objects.create(**vehicle)
        print('Successfully loaded vehicle db...')

        Landfill.objects.create(
            address="Amin Bazar",
            capacity=3500,
            latitude=23.79795912830887,
            longitude=90.30016736544847,
        )
