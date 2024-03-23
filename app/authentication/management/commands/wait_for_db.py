import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database available"""

    def handle(self, *args, **options):
        self.stdout.write(' waiting for database... ')
        time.sleep(5)
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(' Database unavailable, waiting 5 sec... ')
                time.sleep(5)
        self.stdout.write(self.style.SUCCESS('Database available!'))
