from django.contrib import admin
from .models import STS, Vehicle, Landfill, STSManager


class LandfillAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'capacity', 'latitude',
                    'longitude')
    list_per_page = 20


admin.site.register(Landfill, LandfillAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_number', 'type',
                    'capacity', 'loaded_fuel_cost_per_km', 'unloaded_fuel_cost_per_km')
    search_fields = ('vehicle_number', 'type', 'capacity')
    list_per_page = 20


admin.site.register(Vehicle, VehicleAdmin)


class STSAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'ward', 'address', 'capacity',
                    'latitude', 'longitude')
    search_fields = ('address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)


class STSManagerAdmin(admin.ModelAdmin):
    list_display = ('id', 'sts', 'user')
    search_fields = ('user', 'sts')
    list_per_page = 20


admin.site.register(STSManager, STSManagerAdmin)
