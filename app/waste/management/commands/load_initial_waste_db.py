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

        # for sts in STS.objects.all():
        #     for landfill in Landfill.objects.all():
        #         OptimizeForList = ['FastestRoute', 'ShortestRoute']
        #         for OptimizeFor in OptimizeForList:
        #             if Path.objects.filter(
        #                 sts=sts,
        #                 landfill=landfill,
        #                 OptimizeFor=OptimizeFor
        #             ).exists():
        #                 continue
        #             res = aws_map_route_api(
        #                 source_lat=sts.latitude,
        #                 source_lon=sts.longitude,
        #                 dest_lat=landfill.latitude,
        #                 dest_lon=landfill.longitude,
        #                 OptimizeFor=OptimizeFor
        #             )
        #             DriveDistance = res['DriveDistance']
        #             DistanceUnit = res['DistanceUnit']
        #             DriveTime = res['DriveTime']
        #             TimeUnit = res['TimeUnit']
        #             PathList = json.dumps({"PathList": res['PathList']})
        #             path, created = Path.objects.get_or_create(
        #                 sts=sts,
        #                 landfill=landfill,
        #                 OptimizeFor=OptimizeFor,
        #                 DriveDistance=DriveDistance,
        #                 DistanceUnit=DistanceUnit,
        #                 DriveTime=DriveTime,
        #                 TimeUnit=TimeUnit,
        #                 points=PathList
        #             )
        #             print(sts, landfill, path)
        #             # for p in PathList:
        #             #     point, created = Point.objects.get_or_create(
        #             #         latitude=p[1], longitude=p[0])
        #             #     path.points.add(point.id)
        #             return
