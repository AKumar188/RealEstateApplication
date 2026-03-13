from django.contrib import admin
from .models import UserSubscription,SubscriptionPlan


admin.site.register(SubscriptionPlan)
admin.site.register(UserSubscription)
