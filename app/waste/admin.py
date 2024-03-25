from django.contrib import admin
from .models import STS, Vehicle, Landfill


class LandfillAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'capacity', 'latitude',
                    'longitude', 'manager')
    list_per_page = 20


admin.site.register(Landfill, LandfillAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'vehicle_number', 'type', 'capacity')
    search_fields = ('vehicle_number', 'type', 'capacity')
    list_per_page = 20


admin.site.register(Vehicle, VehicleAdmin)


class STSAdmin(admin.ModelAdmin):
    list_display = ('id', 'zone', 'ward', 'address', 'capacity',
                    'latitude', 'longitude', 'manager')
    search_fields = ('address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)
