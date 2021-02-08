from django.contrib.gis.db import models
from cities.models import City
from prefectures.models import Prefecture

class Farmland(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE)
	geom = models.PolygonField(blank=False, null=False)

	@property
	def centroid(self):
		return self.geom.centroid.coords

	class Meta:
		db_table = "farmlands"
