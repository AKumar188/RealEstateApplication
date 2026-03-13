from django.urls import path
from .views import SubscriptionPlanListView, SubscribeView, MySubscriptionView, CancelSubscriptionView

urlpatterns = [
    # GET plans
    path("plans/", SubscriptionPlanListView.as_view(), name="subscription-plans"),

    #POST subscribe
    path("subscribe/<plan_id>/", SubscribeView.as_view(), name="subscription-subscribe"),

    #GET my subscription
    path("my-subscription/", MySubscriptionView.as_view(), name="usersubscriptionplan"),

    #POST cancel subscription
    path("cancel-subscription/", CancelSubscriptionView.as_view(), name="subscription-cancel"),
]
