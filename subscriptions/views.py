import uuid
from datetime import timedelta

from django.utils.timezone import now

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from .models import SubscriptionPlan, Subscription
from .serializers import SubscriptionPlanSerializer, SubscribeSerializer

from payments.models import Payment
from payments.serializers import PaymentSerializer


# ======================================================
# GET /subscription/plans
# ======================================================
class SubscriptionPlanListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        plans = SubscriptionPlan.objects.filter(is_active=True)

        serializer = SubscriptionPlanSerializer(plans, many=True)

        return Response({
            "success": True,
            "plans": serializer.data
        })


# ======================================================
# POST /subscription/subscribe
# Creates Subscription + Payment (Pending)
# ======================================================
class SubscribeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubscribeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data["plan_id"]

        # Check plan exists
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            return Response(
                {"error": "Plan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Subscription dates
        start_date = now()
        end_date = start_date + timedelta(days=plan.duration_days)

        # Create Subscription as Pending
        subscription = Subscription.objects.create(
            user=request.user,
            plan=plan,
            status="pending",
            start_date=start_date,
            end_date=end_date
        )

        # Create Payment Linked to Subscription
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
                "status": subscription.status,
                "plan": plan.name,
                "start_date": subscription.start_date,
                "end_date": subscription.end_date
            },
            "payment": PaymentSerializer(payment).data
        }, status=status.HTTP_201_CREATED)
