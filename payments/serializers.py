import uuid
from rest_framework import serializers
from .models import Payment
from subscriptions.models import Subscription


# ✅ Payment Output Serializer
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "gateway_transaction_id",
            "status",
            "created_at",
        ]


# ✅ Payment Create Request Serializer
class PaymentCreateSerializer(serializers.Serializer):
    subscription_id = serializers.UUIDField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.CharField(max_length=10)
    gateway = serializers.CharField(max_length=50)

    def validate_subscription_id(self, value):
        if not Subscription.objects.filter(id=value).exists():
            raise serializers.ValidationError("Subscription not found")
        return value
