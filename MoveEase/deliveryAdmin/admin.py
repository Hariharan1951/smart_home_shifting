from django.contrib import admin
from .models import VehicleCapicityTable

# Register your models here.
@admin.register(VehicleCapicityTable)
class VehicleCapacityTable(admin.ModelAdmin):
    list_display = ["vehicle_type", "vehicle_length_feet", "vehicle_load_capacity_kg"]
    