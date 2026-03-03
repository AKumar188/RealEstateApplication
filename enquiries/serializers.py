from rest_framework import serializers
from .models import Enquiry

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = "__all__"
        read_only_fields = ("id", "sender", "owner", "created_at", "updated_at")
        