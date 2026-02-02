from django.contrib import admin
from .models import Hostel
# Register your models here.

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ("name", "capacity", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
