from django.contrib import admin

from .models import Collectors, Courier

@admin.register(Collectors)
class CollectorsAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']
    search_fields = ['username']


@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number']
    search_fields = ['username']
