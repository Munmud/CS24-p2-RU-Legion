from django.contrib import admin
from .models import *


class WasteTransferAdmin(admin.ModelAdmin):
    list_display = [field.name for field in WasteTransfer._meta.fields]
    list_per_page = 20


admin.site.register(WasteTransfer, WasteTransferAdmin)


class LandfillAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Landfill._meta.fields]
    list_per_page = 20


admin.site.register(Landfill, LandfillAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Vehicle._meta.fields]
    search_fields = ('vehicle_number', 'type', 'capacity')
    list_per_page = 20


admin.site.register(Vehicle, VehicleAdmin)


class STSAdmin(admin.ModelAdmin):
    list_display = [field.name for field in STS._meta.fields]
    search_fields = ('address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)


class STSManagerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in STSManager._meta.fields]
    search_fields = ('user', 'sts')
    list_per_page = 20


admin.site.register(STSManager, STSManagerAdmin)
