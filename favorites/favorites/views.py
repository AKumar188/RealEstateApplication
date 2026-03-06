from rest_framework import generics
from .models import Favorite
from .serializers import FavoriteSerializer


# GET list + POST create
class FavoriteListCreateView(generics.ListCreateAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


# DELETE favorite
class FavoriteDeleteView(generics.DestroyAPIView):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer