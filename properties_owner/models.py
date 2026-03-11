import uuid

from django.db import models


class User(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255, unique=True)
	phone = models.CharField(max_length=20, null=True, blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(null=True, blank=True)
	updated_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		db_table = "users"

	def __str__(self):
		return self.email
