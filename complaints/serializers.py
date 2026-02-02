from rest_framework import serializers
from .models import Complaint
from common.constants import UserRole

class ComplaintCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ["id", "title", "description"]

    def create(self, validated_data):
        request = self.context["request"]
        student = request.user

        if student.role != UserRole.STUDENT:
            raise serializers.ValidationError("Only students can create complaints")

        # student must be allocated to a room
        if not hasattr(student, "room_allocation"):
            raise serializers.ValidationError("Student is not allocated to any room")

        hostel = student.room_allocation.room.hostel

        return Complaint.objects.create(
            student=student,
            hostel=hostel,
            **validated_data
        )


class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = "__all__"
        read_only_fields = ["student", "hostel", "created_at"]
