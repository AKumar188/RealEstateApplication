from django.db import models

class Facility(models.Model):
	facility_id = models.AutoField(primary_key=True)
	facility_name = models.CharField(max_length=255)
	facility_description = models.TextField(blank=True)
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = "facility"
		ordering = ["facility_name"]

	def __str__(self):
		return self.facility_name
