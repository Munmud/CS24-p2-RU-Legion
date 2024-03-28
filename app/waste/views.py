
from django.shortcuts import render, redirect, get_object_or_404
from core.utils import is_system_admin, is_sts_manager
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.contrib import messages
from .forms import *
from .models import *


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
