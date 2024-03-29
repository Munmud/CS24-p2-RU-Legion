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

from core.utils import is_system_admin, is_sts_manager, is_landfill_manager
from .forms import *
from .models import *


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
        Paragraph("Volume: {}".format(transfer.volume), custom_style))
    content.append(Paragraph("Amount: {}".format(100), custom_style))

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
def add_waste_transfer(request):
    if request.method == 'POST':
        form = WasteTransferForm(request.POST)
        if form.is_valid():
            landfill = form.cleaned_data['landfill']
            vehicle = form.cleaned_data['vehicle']
            volume = form.cleaned_data['volume']
            user = request.user
            sts = STSManager.objects.filter(user=user).first().sts
            if (volume > vehicle.capacity):
                messages.error(request, 'Can\'t send Overloaded vehicle')
                return redirect('add_waste_transfer')
            new_transfer = WasteTransfer(
                sts=sts, landfill=landfill, vehicle=vehicle, volume=volume)
            new_transfer.status = 'Sending to Landfill'
            new_transfer.departure_from_sts = timezone.now()
            new_transfer.save()
            messages.success(request, f"Sent new Transfer to {landfill}")
            return redirect('add_waste_transfer')
    else:
        form = WasteTransferForm()
    return render(request, 'sts_manager/add_wasteTransfer.html', {'form': form})


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
