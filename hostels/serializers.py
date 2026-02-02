from rest_framework import serializers
from .models import Hostel, WardenHostel
from common.constants import UserRole


class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hostel
        fields = ["id", "name", "address", "capacity", "is_active"]


class WardenHostelAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = WardenHostel
        fields = ["warden", "hostel"]

    def validate(self, attrs):
        warden = attrs["warden"]

        if warden.role != UserRole.WARDEN:
            raise serializers.ValidationError("Only wardens can be assigned to hostels")

        if hasattr(warden, "warden_hostel"):
            raise serializers.ValidationError("Warden already assigned to a hostel")

        return attrs
