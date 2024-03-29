from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

from celery import shared_task


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(
        max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username


@shared_task
def create_profile_offline(username):
    user = User.objects.get(username=username)
    Profile.objects.create(user=user)


@receiver(models.signals.post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        create_profile_offline.delay(instance.username)
