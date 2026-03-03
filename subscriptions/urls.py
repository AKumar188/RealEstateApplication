from django.urls import path
from .views import SubscriptionPlanListView, SubscribeView

urlpatterns = [
    # GET plans
    path("plans/", SubscriptionPlanListView.as_view(), name="subscription-plans"),

    #POST subscribe
    path("subscribe/", SubscribeView.as_view(), name="subscription-subscribe"),
]
