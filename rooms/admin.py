from django.contrib import admin
from .models import Room, RoomAllocation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "room_number", "hostel", "capacity")

@admin.register(RoomAllocation)
class RoomAllocationAdmin(admin.ModelAdmin):
    list_display = ("student", "room")
