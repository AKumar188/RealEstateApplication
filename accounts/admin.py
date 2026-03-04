from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "full_name",
        "role",
        "is_verified",
        "is_staff",
        "is_active",
        "created_at",
    )

    list_filter = ("role", "is_staff", "is_active", "is_verified")

    ordering = ("-created_at",)

    search_fields = ("email", "full_name", "phone")

    readonly_fields = ("created_at", "updated_at", "deleted_at", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "phone", "bio", "avatar_url")}),
        ("Role & Status", {"fields": ("role", "is_verified")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important Dates", {"fields": ("last_login", "created_at", "updated_at", "deleted_at")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )


admin.site.register(User, CustomUserAdmin)