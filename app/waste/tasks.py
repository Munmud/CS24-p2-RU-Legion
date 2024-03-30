import json
from time import sleep
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db import transaction
from .models import WasteTransferQueue, WasteTransfer


@shared_task
def queue_to_waste_transfer():
    pending_in_queue = WasteTransferQueue.objects.filter(
        status='Pending').all()

    for transfer in pending_in_queue:
        print("transfer", transfer)
        with transaction.atomic():
            if transfer.vehicle.status != 'Available':
                continue
            new_transfer = WasteTransfer(
                sts=transfer.sts,
                landfill=transfer.landfill,
                vehicle=transfer.vehicle,
                path=transfer.path,
                volume=transfer.volume
            )
            print("new_transfer", new_transfer)
            new_transfer.status = 'Sending to Landfill'
            new_transfer.departure_from_sts = timezone.now()
            new_transfer.save()
            transfer.status = 'Completed'
            transfer.save()


def schedule_task():
    interval, _ = IntervalSchedule.objects.get_or_create(
        every=30,
        period=IntervalSchedule.SECONDS
    )

    PeriodicTask.objects.create(
        interval=interval,
        name='fleetChecking',
        task="waste.tasks.queue_to_waste_transfer",
        # args=json.dumps(["Arg1", "Arg2"])
        # one_off=True
    )

    return "Task Scheduled!"
