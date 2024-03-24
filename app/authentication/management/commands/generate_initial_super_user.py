
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

USER_USER1 = 'user1'
USER_USER2 = 'user2'
USER_ADMIN = 'admin'
PASSWORD = 'pass'
GROUP_SYSTEM_ADMIN = 'System Admin'
GROUP_STS_MANAGER = 'STS Manager'
GROUP_LANDFILL_MANAGER = 'Landfill Manager'


def create_general_users(self):
    users_data = [
        {'username': USER_USER1, 'password': PASSWORD},
        {'username': USER_USER2, 'password': PASSWORD},
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
    username = USER_ADMIN
    password = PASSWORD

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password)
        self.stdout.write(self.style.SUCCESS(
            f'Superuser\n\t email:\t\t {username}\n\t password:\t {password}'))
    else:
        self.stdout.write(self.style.WARNING(
            f'User {username} already exists. Skipping...'))


def create_groups(self):
    group_names = [
        GROUP_SYSTEM_ADMIN,
        GROUP_STS_MANAGER,
        GROUP_LANDFILL_MANAGER
    ]
    for group in group_names:
        if not Group.objects.filter(name=group).exists():
            group, created = Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(
                f'Group : {group} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Group : {group} already exists. Skipping...'))


def add_user1_to_system_admin_group(self):
    librarian_user = User.objects.get(username=USER_USER1)
    system_admin_group = Group.objects.get(name=GROUP_SYSTEM_ADMIN)
    librarian_user.groups.add(system_admin_group)


class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        create_general_users(self)
        create_super_user(self)
        create_groups(self)
        add_user1_to_system_admin_group(self)
