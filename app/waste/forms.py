from django import forms
from .models import Vehicle


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'type', 'capacity',
                  'loaded_fuel_cost_per_km', 'unloaded_fuel_cost_per_km']
