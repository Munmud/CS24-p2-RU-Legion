
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates initial groups'

    def handle(self, *args, **kwargs):
        group_names = [
            'System Admin',
            'STS Manager',
            'Landfill Manager',
        ]
        for group in group_names:
            if not Group.objects.filter(name=group).exists():
                group, created = Group.objects.get_or_create(name=group)
                self.stdout.write(self.style.SUCCESS(
                    f'Group {group} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Group {group} already exists'))
                # models = [Book, Category, Reservation, Bill]

                # for model in models:
                #     content_type = ContentType.objects.get_for_model(model)
                #     permissions = Permission.objects.filter(
                #         content_type=content_type)
                #     group.permissions.add(*permissions)

                # librarian_user.groups.add(group)
                # librarian_user.is_staff = True
                # librarian_user.save()
