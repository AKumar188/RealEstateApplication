from django.urls import path

from .views import FacilityListView

urlpatterns = [
    path("", FacilityListView.as_view(), name="facility-list"),
]
