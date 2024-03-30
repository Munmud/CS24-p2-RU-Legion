import json
from time import sleep
from celery import shared_task
from django.conf import settings
from django_celery_beat.models import PeriodicTask, IntervalSchedule


# @shared_task
# def my_task():
#     for i in range(11):
#         print(i)
#         sleep(1)
#     return "Task Complete!"


# def schedule_task():
#     interval, _ = IntervalSchedule.objects.get_or_create(
#         every=30,
#         period=IntervalSchedule.SECONDS
#     )

#     PeriodicTask.objects.create(
#         interval=interval,
#         name='munmud-first-schedule',
#         task="report.tasks.my_task",
#         # args=json.dumps(["Arg1", "Arg2"])
#         # one_off=True
#     )

# return "Task Scheduled!"
