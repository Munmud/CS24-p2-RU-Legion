# Generated by Django 5.0.1 on 2024-03-26 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waste', '0002_alter_landfill_latitude_alter_landfill_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='landfill',
            name='latitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='landfill',
            name='longitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sts',
            name='latitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sts',
            name='longitude',
            field=models.CharField(max_length=20),
        ),
    ]