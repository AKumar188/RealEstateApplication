from django.urls import path
from .views import (
    CreatePaymentView,
    MyPaymentsView,
    AllPaymentsAdminView,
    UpdatePaymentStatusView,
    PaymentWebhookView
)

urlpatterns = [
    path("create/", CreatePaymentView.as_view()),
    path("my/", MyPaymentsView.as_view()),
    path("admin/all/", AllPaymentsAdminView.as_view()),
    path("<uuid:pk>/status/", UpdatePaymentStatusView.as_view()),
    path("webhook/", PaymentWebhookView.as_view()),
]
