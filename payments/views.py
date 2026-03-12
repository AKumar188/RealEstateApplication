import uuid
import razorpay

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings

from .models import Payment
from subscriptions.models import Subscription
from .serializers import PaymentSerializer, PaymentCreateSerializer


# ======================================================
# CREATE PAYMENT (RAZORPAY ORDER CREATION)
# ======================================================

class CreatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subscription = Subscription.objects.get(
                id=serializer.validated_data["subscription_id"]
            )
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Subscription not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if subscription.user != request.user:
            return Response(
                {"error": "You cannot pay for another user's subscription"},
                status=status.HTTP_403_FORBIDDEN
            )

        # Prevent duplicate pending payments
        if Payment.objects.filter(subscription=subscription, status="pending").exists():
            return Response(
                {"error": "Payment already pending for this subscription"},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = serializer.validated_data["amount"]

        # Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        # Create Razorpay Order
        order = client.order.create({
            "amount": int(amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=amount,
            currency="INR",
            gateway="razorpay",
            gateway_transaction_id=order["id"],
            status="pending"
        )

        return Response(
            {
                "success": True,
                "message": "Razorpay order created",
                "order_id": order["id"],
                "razorpay_key": settings.RAZORPAY_KEY_ID,
                "payment": PaymentSerializer(payment).data
            },
            status=status.HTTP_201_CREATED
        )


# ======================================================
# VERIFY RAZORPAY PAYMENT
# ======================================================

class VerifyRazorpayPayment(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        payment_id = request.data.get("razorpay_payment_id")
        order_id = request.data.get("razorpay_order_id")

        try:
            payment = Payment.objects.get(
                gateway_transaction_id=order_id
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=404)

        payment.gateway_transaction_id = payment_id
        payment.status = "success"
        payment.save()

        # Activate subscription
        payment.subscription.status = "active"
        payment.subscription.save()

        return Response({
            "success": True,
            "message": "Payment verified successfully",
            "payment": PaymentSerializer(payment).data
        })


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

        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response({
            "success": True,
            "message": "Payment status updated",
            "payment": PaymentSerializer(payment).data
        })


# ======================================================
# PAYMENT WEBHOOK
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

        if new_status == "success":
            payment.subscription.status = "active"
            payment.subscription.save()

        return Response({
            "success": True,
            "message": "Webhook processed successfully",
            "payment": PaymentSerializer(payment).data
        })