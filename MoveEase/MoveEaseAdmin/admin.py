from django.contrib import admin
from .models import ItemsTable, CouponCodeTable, OrderReceived

# Register your models here.

@admin.register(ItemsTable)
class ItemsTableAdmin(admin.ModelAdmin):
    list_display=["item_name", "item_weight_kg", "item_size_ft"]

admin.site.register(CouponCodeTable)
admin.site.register(OrderReceived)