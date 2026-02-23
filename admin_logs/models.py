from django.db import models


class block(models.Model):
    id = models.BigAutoField(primary_key=True)
    blocked_user_id = models.BooleanField(default=False)


class properties(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    listing_type = models.CharField(max_length=50)
    property_type = models.CharField(max_length=50)
    bedrooms = models.PositiveIntegerField(default=0)
    bathrooms = models.PositiveIntegerField(default=0)
    area_sqft = models.PositiveIntegerField(default=0)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    pincode = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "pending"),
            ("approved", "approved"),
            ("rejected", "rejected"),
        ],
        default="pending",
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class users(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="user")
    full_name = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
