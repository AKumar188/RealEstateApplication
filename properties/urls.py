from django.urls import path
from .views import (
    create_property,
    search_properties,
    property_detail,
    update_property,
    delete_property,
    my_listings
)

urlpatterns = [
    path('create/', create_property),
    path('', search_properties),  # list + search
    path('<int:id>/', property_detail),
    path('<int:id>/update/', update_property),
    path('<int:id>/delete/', delete_property),
    path('my/', my_listings),
]