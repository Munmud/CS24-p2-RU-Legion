from django.contrib import admin
from .models import STS, Vehicle, Landfill


class LandfillAdmin(admin.ModelAdmin):
    list_display = ('id', 'Address', 'Capacity', 'Latitude',
                    'Longitude', 'Landfill_Manager_ID')
    list_per_page = 20


admin.site.register(Landfill, LandfillAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_number', 'type', 'capacity')
    search_fields = ('vehicle_number', 'type', 'capacity')
    list_per_page = 20


admin.site.register(Vehicle, VehicleAdmin)


class STSAdmin(admin.ModelAdmin):
    list_display = ('id', 'Zone', 'Ward', 'Address', 'Capacity',
                    'Latitude', 'Longitude', 'STS_Manager_ID')
    search_fields = ('Address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)
