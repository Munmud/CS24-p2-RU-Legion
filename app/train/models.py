from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import F, Value

# Create your models here.
class TrainUser(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=255)
    balance = models.PositiveIntegerField()

class Wallet(models.Model):
    wallet_id = models.IntegerField(primary_key=True)  # Assuming wallet_id is the primary key
    balance = models.PositiveIntegerField()
    wallet_user = models.OneToOneField(TrainUser, on_delete=models.CASCADE)

class Station(models.Model):
    station_id = models.IntegerField(primary_key=True)
    station_name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.station_name

class Train(models.Model):
    train_id = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.train_name} (ID: {self.train_id})"

    def trains_at_station(self, station_id):
        # Get stops at the given station
        stops_at_station = Stop.objects.filter(station_id=station_id)
        
        # Sort stops by departure time and arrival time
        stops_at_station = stops_at_station.annotate(
            departure_time_null_last=Coalesce('departure_time', Value('9999-12-31 23:59:59')),
            arrival_time_null_last=Coalesce('arrival_time', Value('9999-12-31 23:59:59'))
        ).order_by('departure_time_null_last', 'arrival_time_null_last')

        # Get unique trains and sort them
        trains = []
        seen_train_ids = set()
        for stop in stops_at_station:
            if stop.train_id not in seen_train_ids:
                trains.append(stop.train)
                seen_train_ids.add(stop.train_id)

        return trains

class Stop(models.Model):
    train = models.ForeignKey(Train, related_name='stops', on_delete=models.CASCADE)
    station_id = models.ForeignKey(Station, on_delete=models.CASCADE)
    arrival_time = models.CharField(max_length=50, null=True)
    departure_time = models.CharField(max_length=50, null=True)
    fare = models.PositiveIntegerField()

    def __str__(self):
        return f"Stop at station {self.station_id} for train {self.train.train_name}"

class Route(models.Model):
    from_station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        related_name='routes_from'
    )
    to_station = models.ForeignKey(
        'Station',
        on_delete=models.CASCADE,
        related_name='routes_to'
    )
    fare = models.PositiveIntegerField()
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)


   
