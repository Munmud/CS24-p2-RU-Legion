from django.db import models
from django.contrib.auth.models import User


class STS(models.Model):
    Zone = models.IntegerField()
    Ward = models.IntegerField()
    Address = models.CharField(max_length=255)
    Capacity = models.IntegerField()
    Latitude = models.DecimalField(max_digits=9, decimal_places=6)
    Longitude = models.DecimalField(max_digits=9, decimal_places=6)
    STS_Manager_ID = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Sts in {self.Address}"
