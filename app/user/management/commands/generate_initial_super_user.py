# CreateSuperuser.py

from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from core.models import User

class Command(BaseCommand):
    help = 'Creates a superuser'

    # def add_arguments(self, parser):
    #     # parser.add_argument('--username', type=str, help='Username for the superuser', required=True)
    #     parser.add_argument('--email', type=str, help='Email for the superuser', required=True)
    #     parser.add_argument('--password', type=str, help='Password for the superuser', required=True)

    def handle(self, *args, **kwargs):
        # username = kwargs['username']
        email = 'm@gmail.com'
        password = 'pass'

        user = User.objects.create_superuser(email=email, password=password)

        self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully.'))
