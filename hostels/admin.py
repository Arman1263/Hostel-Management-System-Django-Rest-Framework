from django.contrib import admin
from .models import Hostel, WardenHostel

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

@admin.register(WardenHostel)
class WardenHostelAdmin(admin.ModelAdmin):
    list_display = ("warden", "hostel")
