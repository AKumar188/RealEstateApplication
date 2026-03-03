from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
    "id",
    "email",
    "phone",
    "password",
    "role",
    "full_name",
    "bio",
    "avatar_url",
    "is_verified",
    "is_active",
    "created_at",
    "updated_at",
    "deleted_at",
] 

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user