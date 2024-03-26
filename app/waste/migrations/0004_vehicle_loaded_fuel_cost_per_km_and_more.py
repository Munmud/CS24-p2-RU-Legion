# Generated by Django 5.0.1 on 2024-03-26 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0003_alter_landfill_latitude_alter_landfill_longitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='loaded_fuel_cost_per_km',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='unloaded_fuel_cost_per_km',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]