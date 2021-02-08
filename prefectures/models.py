from django.db import models

class Prefecture(models.Model):
	name = models.CharField(blank=False, null=False, unique=True, max_length=255)

	class Meta:
		db_table = "prefectures"

	def __str__(self):
		return self.name
