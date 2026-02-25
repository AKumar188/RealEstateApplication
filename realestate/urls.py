from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [

    path('admin/', admin.site.urls),

    # Payments
    path("api/v1/payments/", include("payments.urls")),

    # Subscriptions
    path("subscription/", include("subscriptions.urls")),

    # Notifications
    path("notification/", include("notifications.urls")),

    # JWT Authentication
    path("api/token/", TokenObtainPairView.as_view(), name="token_login"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

]