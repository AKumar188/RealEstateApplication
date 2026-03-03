from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ['id', 'property', 'created_at']
        read_only_fields = ['id', 'created_at']