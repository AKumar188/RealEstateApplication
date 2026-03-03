from django.contrib import admin
from .models import Review

admin.site.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "property",
        "reviewer",
        "rating",
        "created_at"
    )

    search_fields = (
        "property__title",
        "reviewer__email"
    )

    list_filter = (
        "rating",
        "created_at"
    )