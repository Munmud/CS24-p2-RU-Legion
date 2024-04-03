import os
import random
# from tqdm import tqdm
import json
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from core.utils import load_sts, load_vehicle, aws_map_route_api
from waste.models import *


class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        cc = 0
        for sts in load_sts():
            STS.objects.get_or_create(**sts)
            cc += 1
        print(f'Successfully loaded {cc} STS into db...')

        cc = 0
        for vehicle in load_vehicle():
            Vehicle.objects.get_or_create(**vehicle)
            cc += 1
        print(f'Successfully loaded {cc} Vehicle into db...')

        Landfill.objects.get_or_create(
            address="Amin Bazar Landfill",
            capacity=3500,
            latitude=23.79795912830887,
            longitude=90.30016736544847,
        )
        print(f'Successfully loaded 1 Landfill into db...')
