
from django.shortcuts import render, redirect
from core.utils import is_system_admin, is_sts_manager
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
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
            new_transfer = WasteTransfer(
                sts=sts, landfill=landfill, vehicle=vehicle, volume=volume)
            new_transfer.departure = timezone.now()
            new_transfer.save()

            return redirect('dashboard')
    else:
        form = WasteTransferForm()
    return render(request, 'sts_manager/add_wasteTransfer.html', {'form': form})
