from django.contrib import admin
from .models import Property, PropertyImage, PropertyAmenity


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyAmenityInline(admin.TabularInline):
    model = PropertyAmenity
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "price",
        "listing_type",
        "property_type",
        "status",
        "city",
        "created_at"
    )

    search_fields = ("title", "city", "state")

    list_filter = ("listing_type", "property_type", "status")

    inlines = [PropertyImageInline, PropertyAmenityInline]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):

    list_display = (
        "property",
        "image_url",
        "is_primary",
        "created_at"
    )


@admin.register(PropertyAmenity)
class PropertyAmenityAdmin(admin.ModelAdmin):

    list_display = (
        "property",
        "amenity_name"
    )