import uuid
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from .models import Payment
from subscriptions.models import Subscription
from .serializers import PaymentSerializer, PaymentCreateSerializer


# ======================================================
# CREATE PAYMENT (Pending)
# ======================================================
class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Subscription must exist
        try:
            subscription = Subscription.objects.get(
                id=serializer.validated_data["subscription_id"]
            )
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # User must own subscription
        if subscription.user != request.user:
            return Response(
                {"error": "You cannot pay for another user's subscription"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Prevent duplicate pending payment
        if Payment.objects.filter(subscription=subscription, status="pending").exists():
            return Response(
                {"error": "Payment already pending for this subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create Payment Record
        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=serializer.validated_data["amount"],
            currency=serializer.validated_data["currency"],
            gateway=serializer.validated_data["gateway"],
            gateway_transaction_id=str(uuid.uuid4()),
            status="pending"
        )

        return Response(
            {
                "success": True,
                "message": "Payment created successfully",
                "payment": PaymentSerializer(payment).data,
            },
            status=status.HTTP_201_CREATED
        )


# ======================================================
# USER PAYMENT HISTORY
# ======================================================
class MyPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)


# ======================================================
# ADMIN: ALL PAYMENTS
# ======================================================
class AllPaymentsAdminView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset = Payment.objects.all().order_by("-created_at")


# ======================================================
# ADMIN UPDATE PAYMENT STATUS
# ======================================================
class UpdatePaymentStatusView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, pk):
        try:
            payment = Payment.objects.get(id=pk)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        new_status = request.data.get("status")

        allowed_status = ["pending", "success", "failed", "refunded"]

        if new_status not in allowed_status:
            return Response(
                {"error": f"Invalid status. Allowed: {allowed_status}"},
                status=400
            )

        payment.status = new_status
        payment.save()

        # Activate subscription if payment success
        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response(
            {
                "success": True,
                "message": "Payment status updated successfully",
                "payment": PaymentSerializer(payment).data,
            }
        )


# ======================================================
# PAYMENT WEBHOOK (Gateway Simulation)
# ======================================================
class PaymentWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        secret = request.headers.get("X-WEBHOOK-SECRET")

        if secret != settings.PAYMENT_WEBHOOK_SECRET:
            return Response(
                {"error": "Invalid webhook secret"},
                status=403
            )

        payment_id = request.data.get("payment_id")
        new_status = request.data.get("status")

        allowed_status = ["success", "failed"]

        if new_status not in allowed_status:
            return Response(
                {"error": f"Invalid status. Allowed: {allowed_status}"},
                status=400
            )

        try:
            payment = Payment.objects.get(id=payment_id)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        payment.status = new_status
        payment.save()

        # Activate subscription if success
        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response({
            "success": True,
            "message": "Webhook processed successfully",
            "payment": PaymentSerializer(payment).data
        })
