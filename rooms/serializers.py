from rest_framework import serializers
from .models import Room
from django.db.models import Count
from .models import RoomAllocation
from common.constants import UserRole


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["id", "hostel", "room_number", "capacity", "is_active"]

    def validate_capacity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Room capacity must be greater than 0")
        return value


class RoomAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAllocation
        fields = ["id", "student", "room"]

    def validate(self, attrs):
        room = attrs["room"]
        student = attrs["student"]

        # ensure user is student
        if student.role != UserRole.STUDENT:
            raise serializers.ValidationError("Only students can be allocated rooms")

        # check if student already has a room
        if hasattr(student, "room_allocation"):
            raise serializers.ValidationError("Student already allocated to a room")

        # check room capacity
        current_occupancy = room.allocations.count()
        if current_occupancy >= room.capacity:
            raise serializers.ValidationError("Room is already full")

        return attrs
