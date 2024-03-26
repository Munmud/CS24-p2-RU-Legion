
from django.shortcuts import render, redirect
from .forms import VehicleForm
from core.utils import is_system_admin
from django.contrib.auth.decorators import user_passes_test


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
