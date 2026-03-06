from rest_framework import serializers
from .models import SubscriptionPlan, Subscription


# Subscription Plan Serializer
class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = [
            "id",
            "name",
            "price",
            "duration_days",
            "property_limit",
            "is_active",
            "created_at",
        ]


# Subscribe Request Serializer
class SubscribeSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField()

    def validate_plan_id(self, value):
        # Ensure plan exists and active
        if not SubscriptionPlan.objects.filter(id=value, is_active=True).exists():
            raise serializers.ValidationError("Plan not found or inactive.")
        return value