import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics
from django.conf import settings

from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer
from subscriptions.models import UserSubscription


class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subscription = UserSubscription.objects.get(
                id=serializer.validated_data["subscription_id"]
            )
        except UserSubscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=status.HTTP_404_NOT_FOUND)

        if subscription.user != request.user:
            return Response({"error": "Cannot pay for another user's subscription"}, status=status.HTTP_403_FORBIDDEN)

        if Payment.objects.filter(subscription=subscription, status="pending").exists():
            return Response({"error": "Payment already pending"}, status=status.HTTP_400_BAD_REQUEST)

        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=serializer.validated_data["amount"],
            currency=serializer.validated_data["currency"],
            gateway=serializer.validated_data["gateway"],
            gateway_transaction_id=str(uuid.uuid4()),
            status="pending"
        )

        return Response({"success": True, "payment": PaymentSerializer(payment).data}, status=status.HTTP_201_CREATED)


class MyPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


class AllPaymentsAdminView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Payment.objects.all().order_by("-created_at")


class UpdatePaymentStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        new_status = request.data.get("status")
        if new_status not in ["pending", "success", "failed", "refunded"]:
            return Response({"error": "Invalid status"}, status=400)

        payment.status = new_status
        payment.save()

        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response({"success": True, "payment": PaymentSerializer(payment).data})
    
class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        secret = request.headers.get("X-WEBHOOK-SECRET")
        if secret != settings.PAYMENT_WEBHOOK_SECRET:
            return Response({"error": "Invalid webhook secret"}, status=403)

        payment_id = request.data.get("payment_id")
        new_status = request.data.get("status")

        if new_status not in ["success", "failed"]:
            return Response({"error": "Invalid status. Allowed: success, failed"}, status=400)


        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        payment.status = new_status
        payment.save()

        # Activate subscription if payment succeeded
        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response({
            "success": True,
            "message": "Webhook processed successfully",
            "payment": PaymentSerializer(payment).data
        })