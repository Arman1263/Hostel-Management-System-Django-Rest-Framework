from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("email", "full_name")
