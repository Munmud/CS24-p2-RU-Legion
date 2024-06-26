# Generated by Django 5.0.1 on 2024-03-29 10:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=20, unique=True)),
                ('type', models.CharField(choices=[('Open Truck', 'Open Truck'), ('Dump Truck', 'Dump Truck'), ('Compactor', 'Compactor'), ('Container Carrier', 'Container Carrier')], max_length=20)),
                ('capacity', models.IntegerField(choices=[(1, '1 ton'), (2, '2 ton'), (3, '3 ton'), (4, '4 ton'), (5, '5 ton'), (6, '6 ton'), (7, '7 ton'), (8, '8 ton'), (9, '9 ton'), (10, '10 ton'), (11, '11 ton'), (12, '12 ton'), (13, '13 ton'), (14, '14 ton'), (15, '15 ton')])),
                ('loaded_fuel_cost_per_km', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('unloaded_fuel_cost_per_km', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('status', models.CharField(choices=[('Available', 'Available'), ('Inactive', 'Inactive'), ('Under Maintenance', 'Under Maintenance'), ('In Transit', 'In Transit')], default='Available', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Landfill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('latitude', models.CharField(max_length=20)),
                ('longitude', models.CharField(max_length=20)),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
        migrations.CreateModel(
            name='STS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.IntegerField()),
                ('ward', models.IntegerField()),
                ('address', models.CharField(max_length=255)),
                ('capacity', models.IntegerField()),
                ('latitude', models.CharField(max_length=20)),
                ('longitude', models.CharField(max_length=20)),
            ],
            options={
                'unique_together': {('latitude', 'longitude')},
            },
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.TextField()),
                ('OptimizeFor', models.CharField(choices=[('FastestRoute', 'FastestRoute'), ('ShortestRoute', 'ShortestRoute')], max_length=20)),
                ('AvoidTolls', models.BooleanField(default=False)),
                ('DriveDistance', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('DistanceUnit', models.CharField(blank=True, max_length=20, null=True)),
                ('DriveTime', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TimeUnit', models.CharField(blank=True, max_length=20, null=True)),
                ('landfill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.landfill')),
                ('sts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.sts')),
            ],
            options={
                'unique_together': {('sts', 'landfill', 'OptimizeFor', 'AvoidTolls')},
            },
        ),
        migrations.CreateModel(
            name='WasteTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('volume', models.DecimalField(decimal_places=2, max_digits=10)),
                ('departure_from_sts', models.DateTimeField(null=True)),
                ('departure_from_landfill', models.DateTimeField(null=True)),
                ('arrival_at_landfill', models.DateTimeField(null=True)),
                ('arrival_at_sts', models.DateTimeField(null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Sending to Landfill', 'Sending to Landfill'), ('Dumping in Landfill', 'Dumping in Landfill'), ('Returning to STS', 'Returning to STS'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('landfill', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='waste.landfill')),
                ('path', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.path')),
                ('sts', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='waste.sts')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='waste.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='LandfillManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('landfill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.landfill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user',)},
            },
        ),
        migrations.CreateModel(
            name='STSManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waste.sts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user',)},
            },
        ),
    ]
