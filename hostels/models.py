# Create your models here.
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()

    capacity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_hostels"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WardenHostel(models.Model):
    warden = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="warden_hostel"
    )

    hostel = models.OneToOneField(
        Hostel,
        on_delete=models.CASCADE,
        related_name="assigned_warden"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.warden} → {self.hostel}"
