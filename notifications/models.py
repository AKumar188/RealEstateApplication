import uuid
from django.db import models
from django.utils import timezone
from accounts.models import User


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    type = models.CharField(max_length=30)
    title = models.CharField(max_length=255)
    body = models.TextField()
    reference_id = models.UUIDField()

    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
