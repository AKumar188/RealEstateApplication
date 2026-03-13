from rest_framework import serializers
from .models import SubscriptionPlan, UserSubscription

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price', 'duration_days', 'property_limit', 'is_active', 'created_at']


# Serializer for subscribing to a plan
class SubscribeSerializer(serializers.Serializer):
    plan_id = serializers.UUIDField()