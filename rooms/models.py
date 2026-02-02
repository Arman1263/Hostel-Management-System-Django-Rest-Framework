from django.db import models
from hostels.models import Hostel

from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL



class Room(models.Model):
    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="rooms"
    )

    room_number = models.CharField(max_length=20)
    capacity = models.PositiveIntegerField()

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("hostel", "room_number")

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"


class RoomAllocation(models.Model):
    student = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="room_allocation"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    allocated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "room")

    def __str__(self):
        return f"{self.student} → {self.room}"
