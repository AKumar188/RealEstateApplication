from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.

from django.contrib.auth.mixins import LoginRequiredMixin

class NotificationListView(LoginRequiredMixin, APIView):
    permission_classes = []

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)
    
class MarkNotificationReadView(APIView):
    permission_classes = []

    def patch(self, request, id):
        notification = get_object_or_404(Notification,
                                          id=id, 
                                          user=request.user)
        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read"})