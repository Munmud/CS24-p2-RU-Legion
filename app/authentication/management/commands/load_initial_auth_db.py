
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.conf import settings

from core.utils import create_system_admin
from waste.models import WasteTransfer, STS, STSManager, Landfill, LandfillManager

USER_USER1 = 'user1'
USER_USER2 = 'user2'
USER_ADMIN = 'admin'
PASSWORD = 'pass'


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

    return [USER_USER1, USER_USER2]


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
    user, _ = User.objects.get_or_create(username=username, password=password)
    return user


def create_groups(self):
    group_names = [
        settings.GROUP_NAME_SYSTEM_ADMIN,
        settings.GROUP_NAME_STS_MANAGER,
        settings.GROUP_NAME_LANDFILL_MANAGER
    ]
    for group in group_names:
        if not Group.objects.filter(name=group).exists():
            group, created = Group.objects.get_or_create(name=group)
            self.stdout.write(self.style.SUCCESS(
                f'Group : {group} created successfully'))
        else:
            self.stdout.write(self.style.WARNING(
                f'Group : {group} already exists. Skipping...'))


def add_permissions_to_system_admin_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_SYSTEM_ADMIN)

    # Get all available content types (models)
    content_types = ContentType.objects.all()

    # Get all permissions for each model and add them to the system_admin group
    for content_type in content_types:
        permissions = Permission.objects.filter(content_type=content_type)
        group.permissions.add(*permissions)


def add_permissions_to_sts_manager_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_STS_MANAGER)
    content_type = ContentType.objects.get_for_model(WasteTransfer)
    permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.add(*permissions)


def add_permissions_to_landfill_manager_group(self):
    group = Group.objects.get(name=settings.GROUP_NAME_LANDFILL_MANAGER)
    content_type = ContentType.objects.get_for_model(WasteTransfer)
    permissions = Permission.objects.filter(content_type=content_type)
    group.permissions.add(*permissions)


def add_user1_to_system_admin_group(self):
    user = User.objects.get(username=USER_USER1)
    system_admin_group = Group.objects.get(
        name=settings.GROUP_NAME_SYSTEM_ADMIN)
    user.groups.add(system_admin_group)


class Command(BaseCommand):
    help = 'Creates a superuser'

    def handle(self, *args, **kwargs):
        create_groups(self)
        add_permissions_to_system_admin_group(self)
        add_permissions_to_sts_manager_group(self)
        add_permissions_to_landfill_manager_group(self)

        # super_user = create_super_user(self)

        create_system_admin(
            username=USER_ADMIN,
            password=PASSWORD,
        )
        create_general_users(self)
