from rest_framework import serializers

from .models import Facility


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = [
            "facility_id",
            "facility_name",
            "facility_description",
            "is_active",
            "created_at",
            "updated_at",
        ]
