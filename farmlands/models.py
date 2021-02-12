from django.contrib.gis.db import models
from django.db.models import F
from cities.models import City
from prefectures.models import Prefecture
from django.contrib.gis.db.models.functions import Intersection, Union, MakeValid

class Farmland(models.Model):
	city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
	geom = models.PolygonField(blank=False, null=False)

	@property
	def centroid(self):
		return self.geom.centroid.coords
	class Meta:
		db_table = "farmlands"
