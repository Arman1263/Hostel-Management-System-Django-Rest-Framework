from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "hostel", "capacity", "is_active")
    list_filter = ("hostel", "is_active")
    search_fields = ("room_number",)
