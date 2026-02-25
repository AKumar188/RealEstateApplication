import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User
from subscriptions.models import Subscription


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    gateway = models.CharField(max_length=50)
    gateway_transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20)
    ss = models.CharField(max_length=20)

    created_at = models.DateTimeField(default=timezone.now)
