import uuid
from datetime import timedelta
from django.utils.timezone import now
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions, status

from .models import SubscriptionPlan, UserSubscription
from .serializers import SubscriptionPlanSerializer, SubscribeSerializer
from payments.models import Payment
from payments.serializers import PaymentSerializer


class SubscriptionPlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response({"success": True, "plans": serializer.data})


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, plan_id):
        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan_id = serializer.validated_data["plan_id"]

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return Response({"error": "Plan not found"}, status=status.HTTP_404_NOT_FOUND)

        # Create UserSubscription as pending
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            status="pending",
            start_date=now(),
            end_date=now() + timedelta(days=plan.duration_days)
        )

        # Create Payment for subscription
        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=plan.price,
            currency="INR",
            gateway="demo",
            gateway_transaction_id=str(uuid.uuid4()),
            status="pending"
        )

        return Response({
            "success": True,
            "message": "Subscription created. Complete payment to activate.",
            "subscription": {
                "id": str(subscription.id),
                "plan": plan.name,
                "status": subscription.status,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date
            },
            "payment": PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        subscription = UserSubscription.objects.filter(user=request.user, status="active").first()
        if not subscription:
            return Response({"message": "No active subscription"})
        return Response({
            "plan": subscription.plan.name,
            "start_date": subscription.start_date,
            "end_date": subscription.end_date,
            "status": subscription.status
        })


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        subscription = UserSubscription.objects.filter(user=request.user, status="active").first()
        if not subscription:
            return Response({"message": "No active subscription"})
        
        subscription.status = "cancelled"
        subscription.save()
        return Response({"message": "Subscription cancelled successfully"})