from django.shortcuts import render
from django.db.models import Sum
from datetime import timedelta
from django.utils import timezone

from waste.models import WasteTransfer


def admin_generate_waste_transfer_volume_data_last_7_days():
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_volume = data_for_day.aggregate(total_volume=Sum('volume'))[
            'total_volume'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_volume': total_volume,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_volume'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value


def admin_generate_waste_transfer_fuel_cost_data_last_7_days():
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_cost = data_for_day.aggregate(total_cost=Sum('total_cost'))[
            'total_cost'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_cost': total_cost,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_cost'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value


def sts_manager_generate_waste_transfer_volume_data_last_7_days(sts):
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(sts=sts, departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_volume = data_for_day.aggregate(total_volume=Sum('volume'))[
            'total_volume'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_volume': total_volume,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_volume'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value


def sts_manager_generate_waste_transfer_fuel_cost_data_last_7_days(sts):
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(sts=sts, departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_cost = data_for_day.aggregate(total_cost=Sum('total_cost'))[
            'total_cost'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_cost': total_cost,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_cost'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value


def landfill_manager_generate_waste_transfer_volume_data_last_7_days(landfill):
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(landfill=landfill, departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_volume = data_for_day.aggregate(total_volume=Sum('volume'))[
            'total_volume'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_volume': total_volume,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_volume'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value


def landfill_manager_generate_waste_transfer_fuel_cost_data_last_7_days(landfill):
    # Get the start date for the last 7 days
    start_date = timezone.now() - timedelta(days=7)

    # Initialize a dictionary to store the report data
    report_data = {}

    # Iterate over each day in the last 7 days
    for i in range(7):
        # Calculate the start and end of the current day
        current_day_start = start_date + timedelta(days=i)
        current_day_end = current_day_start + timedelta(days=1)

        # Filter the data for the current day
        data_for_day = WasteTransfer.objects.filter(landfill=landfill, departure_from_sts__gte=current_day_start,
                                                    departure_from_sts__lt=current_day_end)

        # Aggregate the volume for the current day
        total_cost = data_for_day.aggregate(total_cost=Sum('total_cost'))[
            'total_cost'] or 0

        # Store the report data for the current day
        report_data[current_day_start.date()] = {
            'total_cost': total_cost,
            'data_points': data_for_day.count()
        }
    report_data_key = [_
                       for _, b in report_data.items()]
    report_data_value = [int(b['total_cost'])
                         for _, b in report_data.items()]
    return report_data_key, report_data_value
