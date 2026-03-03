from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "phone",
        "role",
        "is_verified",
        "is_active",
        "is_staff",
        "created_at"
    )

    search_fields = ("email", "phone", "full_name")

    list_filter = ("role", "is_active", "is_staff", "is_verified")

    ordering = ("-created_at",)

    readonly_fields = ("id", "created_at", "updated_at")