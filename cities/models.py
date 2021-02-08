from django.db import models
from django.contrib.gis.db import models
from prefectures.models import Prefecture

class City(models.Model):
	prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
	name = models.CharField(blank=False, null=False, max_length=255)
	geom = models.MultiPolygonField(blank=False, null=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				name="unique_city",
				fields=["prefecture", "name"]
			)
		]
		db_table = "cities"

	def __str__(self):
		return self.name
