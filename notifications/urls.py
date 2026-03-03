from django.urls import path
from .views import NotificationListView, MarkNotificationReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<uuid:id>/read/', MarkNotificationReadView.as_view(), name='notification-read'),
]