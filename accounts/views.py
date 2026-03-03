from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
# Forgot Password View
class ForgotPasswordView(APIView):
    authentication_classes = []   # No JWT
    permission_classes = []       # Public API

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        reset_link = f"http://localhost:8000/reset-password/?uid={uid}&token={token}"

# In production send email instead
        return Response({
            "message": "Reset link generated successfully",
            "reset_link": reset_link
        }, status=status.HTTP_200_OK)


# Reset Password View
class ResetPasswordView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Password updated successfully"
        }, status=status.HTTP_200_OK)