
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

import random
from datetime import datetime, timedelta
from django.utils import timezone
from waste.models import STS, Landfill, STSManager, LandfillManager, WasteTransfer, Vehicle, Path

USER_USER1 = 'user1'
USER_USER2 = 'user2'
USER_ADMIN = 'admin'
PASSWORD = 'pass'

end_date = timezone.now() - timedelta(days=1)
start_date = end_date - timedelta(days=7)


class Command(BaseCommand):
    help = 'load some waste transfer data'

    def handle(self, *args, **kwargs):

        random_landfill = Landfill.objects.all().order_by('?').first()
        random_sts = STS.objects.all().order_by('?').first()

        STSManager.objects.get_or_create(
            sts=random_sts, user=User.objects.get(username=USER_USER1))
        print(f'Added {USER_USER1} as sts manager ')

        LandfillManager.objects.get_or_create(
            landfill=random_landfill, user=User.objects.get(username=USER_USER2))
        print(f'Added {USER_USER2} as landfill manager')

        for date in (start_date + timedelta(n) for n in range(8)):
            tot = random.randint(5, 10)
            for i in range(tot):
                vehicle = Vehicle.objects.all().order_by('?').first()
                volume = vehicle.capacity-1
                path = Path.objects.filter(
                    sts=random_sts, landfill=random_landfill).order_by('?').first()
                new_transfer = WasteTransfer(
                    sts=random_sts,
                    landfill=random_landfill,
                    vehicle=vehicle,
                    volume=volume,
                    path=path
                )
                new_transfer.status = 'Completed'
                new_transfer.departure_from_sts = date
                new_transfer.save()
