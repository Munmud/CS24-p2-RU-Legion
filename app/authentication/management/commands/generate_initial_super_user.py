
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


def create_general_users(self):
    users_data = [
        {'username': 'user1', 'password': 'pass'},
        {'username': 'user2', 'password': 'pass'},
    ]
    for data in users_data:
        username = data['username']
        password = data['password']
        if not User.objects.filter(username=username).exists():
            User.objects.create_user(username=username, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created user: {username} password: {password}'))
        else:
            self.stdout.write(self.style.WARNING(
                f'User {username} already exists. Skipping...'))


def create_super_user(self):
    username = 'admin'
    password = 'pass'

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Superuser\n\t email:\t\t {username}\n\t password:\t {password}'))
    else:
        self.stdout.write(self.style.WARNING(
            f'User {username} already exists. Skipping...'))


def create_groups(self):
    group_names = [
        'System Admin',
        'STS Manager',
        'Landfill Manager'
    ]
    for group in group_names:
        if not Group.objects.filter(name=group).exists():
            group, created = Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(
                f'Group : {group} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Group : {group} already exists. Skipping...'))


class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        create_general_users(self)
        create_super_user(self)
        create_groups(self)
