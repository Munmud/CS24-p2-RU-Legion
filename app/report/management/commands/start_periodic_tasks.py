
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from waste.tasks import schedule_task


class Command(BaseCommand):
    help = 'start periodic report generation'

    def handle(self, *args, **kwargs):
        res = schedule_task()
        print(res)
