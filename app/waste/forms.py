from django import forms
from .models import Vehicle, WasteTransfer


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'type', 'capacity',
                  'loaded_fuel_cost_per_km', 'unloaded_fuel_cost_per_km']


class WasteTransferForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(WasteTransferForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(
            status='Available')

    class Meta:
        model = WasteTransfer
        fields = ['landfill', 'vehicle',  'volume', ]
