from django import forms
from .models import Vehicle, WasteTransfer


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'type', 'capacity',
                  'loaded_fuel_cost_per_km', 'unloaded_fuel_cost_per_km']


class WasteTransferForm(forms.ModelForm):
    class Meta:
        model = WasteTransfer
        fields = ['landfill', 'vehicle',  'volume', ]
