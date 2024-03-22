# Generated by Django 5.0.1 on 2024-02-09 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrainUser',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=255)),
                ('balance', models.PositiveIntegerField()),
            ],
        ),
    ]
