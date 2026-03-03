from django.urls import path
from .views import ReviewListCreateAPI, ReviewDetailAPI

urlpatterns = [

    path('reviews/', ReviewListCreateAPI.as_view()),
    path('reviews/<uuid:id>/', ReviewDetailAPI.as_view()),

]