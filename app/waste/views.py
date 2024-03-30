from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.contrib import messages
from django.conf import settings

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

    arrival_cost = "{:.2f}".format(transfer.arrival_cost)
    return_cost = "{:.2f}".format(transfer.return_cost)
    total_cost = "{:.2f}".format(transfer.total_cost)

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
    content.append(Paragraph("Capacity: {} ton".format(
        transfer.vehicle.capacity), custom_child_style))
    content.append(Paragraph("Loaded Fuel Cost (per km): {}".format(
        transfer.vehicle.loaded_fuel_cost_per_km), custom_child_style))
    content.append(Paragraph("Unloaded Fuel Cost (per km): {}".format(
        transfer.vehicle.unloaded_fuel_cost_per_km), custom_child_style))

    content.append(Paragraph(
        "Start Journey Time: {}".format(transfer.departure_from_sts), custom_style))
    content.append(Paragraph(
        "Journey Duration: {}".format(transfer.path.DriveTime), custom_style))
    content.append(Paragraph(
        "Journey Distance: {}".format(transfer.path.DriveDistance), custom_style))
    content.append(
        Paragraph("Carried Weight: {} ton".format(transfer.volume), custom_style))
    content.append(
        Paragraph("Truck Arrival Cost: {}".format(arrival_cost), custom_style))
    content.append(
        Paragraph("Truck Return Cost: {}".format(return_cost), custom_style))
    content.append(
        Paragraph("<b>Total Cost: {}</b>".format(total_cost), custom_style))

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


def recommend_fleet(sts, landfill, total_waste):
    path = Path.objects.filter(
        sts=sts,
        landfill=landfill,
        OptimizeFor='FastestRoute'
    ).first()
    available_vehicle = Vehicle.objects.filter(status='Available').all()

    distance = path.DriveDistance
    max_transfer = 0
    for vehicle in available_vehicle:
        max_transfer += 3*vehicle.capacity
    transfer = min(total_waste, max_transfer)

    def knapsack(items, total_carry):
        n = len(items)
        dp = [[0] * (total_carry + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for w in range(1, total_carry + 1):
                if items[i - 1][2] <= w:
                    dp[i][w] = max(items[i - 1][1] + dp[i - 1]
                                   [w - items[i - 1][2]], dp[i - 1][w])
                else:
                    dp[i][w] = dp[i - 1][w]

        # Trace back to find the items selected
        selected_items = []
        total_cost = dp[n][total_carry]
        remaining_carry = total_carry
        for i in range(n, 0, -1):
            if dp[i][remaining_carry] != dp[i - 1][remaining_carry]:
                selected_items.append(items[i - 1][0])
                remaining_carry -= items[i - 1][2]

        return selected_items, total_cost

    items = []
    for vehicle in available_vehicle:
        items.append(((vehicle.vehicle_number, 1),
                      vehicle.loaded_fuel_cost_per_km*distance,
                      vehicle.capacity,
                      ))
        items.append(((vehicle.vehicle_number, 2),
                      vehicle.loaded_fuel_cost_per_km*distance,
                      vehicle.capacity,
                      ))
        items.append(((vehicle.vehicle_number, 3),
                      vehicle.loaded_fuel_cost_per_km*distance,
                      vehicle.capacity,
                      ))

    # print("item-Len", len(items))
    total_carry = transfer
    selected_ids, total_cost = knapsack(items, total_carry)
    # print("Selected IDs:", selected_ids)
    # print("Total Cost:", total_cost)
    selected_car = dict()
    for id in selected_ids:
        if id[0] in selected_car.keys():
            selected_car[id[0]] += 1
        else:
            selected_car[id[0]] = 1
    return selected_car, total_cost


@user_passes_test(is_sts_manager)
def create_fleet_step_1(request):
    if request.method == 'POST':
        total_waste = request.POST.get('total_waste')
        landfill_id = request.POST.get('landfill')

        data = {
            'total_waste': total_waste,
            'landfill_id': landfill_id,
        }

        redirect_url = reverse('create_fleet_step_2') + '?' + \
            '&'.join([f"{key}={value}" for key, value in data.items()])

        return redirect(redirect_url)
    landfills = Landfill.objects.all()

    return render(request, 'sts_manager/add_fleet_step1.html', {
        'landfills': landfills,
    })


@user_passes_test(is_sts_manager)
def create_fleet_step_2(request):
    landfill_id = int(request.GET.get('landfill_id'))
    total_waste = int(request.GET.get('total_waste'))
    vehicles = Vehicle.objects.filter(status='Available').all()
    user = request.user
    sts = STSManager.objects.filter(user=user).first().sts

    landfill = Landfill.objects.get(id=landfill_id)
    recommend_selected_car, recommend_total_cost = recommend_fleet(
        sts, landfill, total_waste)
    # print(recommend_selected_car)
    if request.method == 'POST':
        selected_vehicles = request.POST.getlist(
            'vehicles')
        vehicle_counts = {}
        for vehicle_id in selected_vehicles:
            count_key = 'vehicle_count_' + vehicle_id
            vehicle_id = int(vehicle_id)
            count = request.POST.get(count_key, 0)
            count = int(count)
            vehicle_counts[vehicle_id] = count
            if count < 1:
                current_url = request.get_full_path()
                vehicle = Vehicle.objects.get(id=vehicle_id)
                messages.error(
                    request, f"count must be greater than 0 for {vehicle}")
            if count > 3:
                current_url = request.get_full_path()
                vehicle = Vehicle.objects.get(id=vehicle_id)
                messages.error(
                    request, f"count must be less than 4 for {vehicle}")
                return redirect(current_url)

        for vehicle_id in selected_vehicles:
            vehicle_id = int(vehicle_id)
            cc = vehicle_counts[vehicle_id]
            vehicle = Vehicle.objects.get(id=vehicle_id)
            for i in range(cc):
                WasteTransferQueue.objects.create(
                    sts=sts,
                    landfill=landfill,
                    vehicle=vehicle,
                    volume=vehicle.capacity,
                    path=Path.objects.get(
                        sts=sts, landfill=landfill, OptimizeFor='FastestRoute')
                )
        messages.success(request, 'Added Fleet')
        return redirect('dashboard')

    return render(request, 'sts_manager/add_fleet_step2.html', {
        'vehicles': vehicles,
        'recommend_selected_car': recommend_selected_car
    })
