from rest_framework import generics
from .models import Favorite
from .serializers import FavoriteSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class FavoriteListCreateView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        user = User.objects.first()
        serializer.save(user=user)


class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    lookup_field = "id"