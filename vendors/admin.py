from django.contrib import admin

# Register your models here.
from vendors.models import PurchaseOrder, HistoricalPerformance, Vendor

admin.site.register(Vendor)
admin.site.register(HistoricalPerformance)
admin.site.register(PurchaseOrder)