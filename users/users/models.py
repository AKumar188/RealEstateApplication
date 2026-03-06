import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)   # ✅ added

    role = models.CharField(max_length=50)
    full_name = models.CharField(max_length=255)

    bio = models.TextField(blank=True, null=True)                     # ✅ added
    avatar_url = models.URLField(blank=True, null=True)               # ✅ added

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    deleted_at = models.DateTimeField(blank=True, null=True)          # ✅ added

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email