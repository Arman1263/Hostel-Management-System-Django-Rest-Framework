from django.db import models
from django.conf import settings
from hostels.models import Hostel

User = settings.AUTH_USER_MODEL


class Complaint(models.Model):

    STATUS_OPEN = "OPEN"
    STATUS_IN_PROGRESS = "IN_PROGRESS"
    STATUS_RESOLVED = "RESOLVED"

    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.CASCADE,
        related_name="complaints"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
