from django.contrib import admin
from .models import STS


class STSAdmin(admin.ModelAdmin):
    list_display = ('id', 'Zone', 'Ward', 'Address', 'Capacity',
                    'Latitude', 'Longitude', 'STS_Manager_ID')
    search_fields = ('Address',)
    list_per_page = 20


admin.site.register(STS, STSAdmin)
