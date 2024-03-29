from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.contrib import messages

import io
from django.http import FileResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from django.urls import reverse

from core.utils import (
    is_system_admin,
    is_sts_manager,
    is_landfill_manager
)
from .forms import *
from .models import *


def calculate_fuel_cost(transfer_id):
    transfer = get_object_or_404(WasteTransfer, id=transfer_id)
    carried_volume = transfer.volume

    path = transfer.path
    distance = path.DriveDistance

    vehicle = transfer.vehicle
    loaded_cost = vehicle.loaded_fuel_cost_per_km
    unloaded_cost = vehicle.unloaded_fuel_cost_per_km
    vehicle_capacity = vehicle.capacity

    cost_driving_unloaded = (unloaded_cost*distance)
    cost_driving_loaded = (loaded_cost*distance)

    arrival_cost = cost_driving_unloaded + \
        (cost_driving_loaded-cost_driving_unloaded) * \
        (carried_volume/vehicle_capacity)
    return arrival_cost, cost_driving_unloaded


def waste_transfer_generate_bill(request, transfer_id):
    transfer = WasteTransfer.objects.get(id=transfer_id)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter)
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    custom_style = ParagraphStyle(
        name='CustomStyle', fontSize=14, textColor=colors.black, spaceBefore=20, spaceAfter=10)
    custom_child_style = ParagraphStyle(
        name='CustomStyle', fontSize=14, textColor=colors.black, spaceBefore=10, spaceAfter=10, leftIndent=20)

    arrival_cost, return_cost = calculate_fuel_cost(transfer_id)

    arrival_cost = "{:.2f}".format(arrival_cost)
    return_cost = "{:.2f}".format(return_cost)

    content = []

    content.append(
        Paragraph("{}".format(transfer.landfill), title_style))

    content.append(
        Paragraph("Transfer Id : {}".format(transfer.id), custom_style))

    content.append(
        Paragraph("STS : {}".format(transfer.sts), custom_style))

    content.append(
        Paragraph("Vehicle Details:".format(transfer.vehicle), custom_style))
    content.append(Paragraph("Number: {}".format(
        transfer.vehicle.vehicle_number), custom_child_style))
    content.append(Paragraph("Type: {}".format(
        transfer.vehicle.type), custom_child_style))
    content.append(Paragraph("Capacity: {}".format(
        transfer.vehicle.capacity), custom_child_style))
    content.append(Paragraph("Loaded Fuel Cost (per km): {}".format(
        transfer.vehicle.loaded_fuel_cost_per_km), custom_child_style))
    content.append(Paragraph("Unloaded Fuel Cost (per km): {}".format(
        transfer.vehicle.unloaded_fuel_cost_per_km), custom_child_style))

    content.append(Paragraph(
        "Start Journey Time: {}".format(transfer.departure_from_sts), custom_style))
    content.append(
        Paragraph("Carried Weight: {}".format(transfer.volume), custom_style))
    content.append(
        Paragraph("Truck Arrival Cost: {}".format(arrival_cost), custom_style))
    content.append(
        Paragraph("Truck Return Cost: {}".format(return_cost), custom_style))
    content.append(
        Paragraph("<b>Total Cost: {}</b>".format(return_cost+arrival_cost), custom_style))

    for i in range(5):
        content.append(Paragraph("".format(), custom_style))

    content.append(Paragraph("requested by: {}".format(
        request.user.username), normal_style))
    content.append(Paragraph("printed time: {}".format(
        timezone.now()), normal_style))

    doc.build(content)

    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename=f'trasnfer_{transfer.id}.pdf')


@user_passes_test(is_system_admin)
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a page showing all vehicles
            return redirect('dashboard')
    else:
        form = VehicleForm()
    return render(request, 'system_admin/add_vehicle.html', {'form': form})


@user_passes_test(is_sts_manager)
def waste_transfer_start(request):
    if request.method == 'POST':
        form = WasteTransferForm(request.POST)
        if form.is_valid():
            landfill = form.cleaned_data['landfill']
            vehicle = form.cleaned_data['vehicle']
            volume = form.cleaned_data['volume']
            if (volume > vehicle.capacity):
                messages.error(request, 'Can\'t send Overloaded vehicle')
                return redirect('waste_transfer_start')

            data = {
                'landfill': landfill.id,
                'vehicle': vehicle.id,
                'volume': volume
            }

            redirect_url = reverse('waste_transfer_start_complete') + '?' + \
                '&'.join([f"{key}={value}" for key, value in data.items()])
            print('redirect_url', redirect_url)
            return redirect(redirect_url)
            # user = request.user
            # sts = STSManager.objects.filter(user=user).first().sts

    else:
        form = WasteTransferForm()
    return render(request, 'sts_manager/add_wasteTransfer.html', {'form': form})


@user_passes_test(is_sts_manager)
def waste_transfer_start_complete(request):
    user = request.user
    sts = STSManager.objects.filter(user=user).first().sts
    landfill = get_object_or_404(Landfill, id=request.GET.get('landfill'))
    vehicle = get_object_or_404(Vehicle, id=request.GET.get('vehicle'))
    volume = request.GET.get('volume')

    if request.method == 'POST':
        form = WasteTransferForm_Path(sts, landfill, request.POST)
        if form.is_valid():
            path = form.cleaned_data['path']
            new_transfer = WasteTransfer(
                sts=sts, landfill=landfill, vehicle=vehicle, volume=volume, path=path)
            new_transfer.status = 'Sending to Landfill'
            new_transfer.departure_from_sts = timezone.now()
            new_transfer.save()
            messages.success(request, f"Sent new Transfer to {landfill}")
            return redirect('dashboard')

    form = WasteTransferForm_Path(sts, landfill)
    shortest_path = json.loads(Path.objects.get(
        sts=sts, landfill=landfill, OptimizeFor="ShortestRoute").points)['PathList']

    fastest_path = json.loads(Path.objects.get(
        sts=sts, landfill=landfill, OptimizeFor="FastestRoute").points)['PathList']
    return render(request, 'sts_manager/add_wasteTransfer_complete.html', {
        'form': form,
        'shortest_path': shortest_path,
        'fastest_path': fastest_path,
        'sts': sts,
        'landfill': landfill,
    })


@user_passes_test(is_landfill_manager)
def waste_transfer_start_dumping(request, transfer_id):
    transfer = WasteTransfer.objects.get(id=transfer_id)
    transfer.status = 'Dumping in Landfill'
    transfer.arrival_at_landfill = timezone.now()
    transfer.save()
    return redirect('dashboard')


@user_passes_test(is_landfill_manager)
def waste_transfer_end_dumping(request, transfer_id):
    transfer = WasteTransfer.objects.get(id=transfer_id)
    transfer.departure_from_landfill = timezone.now()
    transfer.status = 'Returning to STS'
    transfer.save()
    return redirect('dashboard')


@user_passes_test(is_sts_manager)
def waste_transfer_complete(request, transfer_id):
    transfer = WasteTransfer.objects.get(id=transfer_id)
    transfer.arrival_at_sts = timezone.now()
    transfer.status = 'Completed'
    transfer.save()
    return redirect('dashboard')

# @user_passes_test(is_sts_manager)
# def edit_waste_transfer(request, transfer_id):
#     transfer = get_object_or_404(WasteTransfer, id=transfer_id)
#     if request.method == 'POST':
#         form = WasteTransferForm(request.POST, instance=transfer)
#         if form.is_valid():
#             form.save()
#             return redirect('dashboard')
#     else:
#         form = WasteTransferForm(instance=transfer)
#     return render(request, 'sts_manager/edit_wasteTransfer.html', {'form': form})

# @user_passes_test(is_sts_manager)
# def approve_transfer(request, transfer_id):
#     transfer = WasteTransfer.objects.get(id=transfer_id)
#     transfer.status = 'Approved'
#     transfer.departure_from_sts = timezone.now()
#     transfer.save()
#     return redirect('dashboard')
