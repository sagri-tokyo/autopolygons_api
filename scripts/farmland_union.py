from chunkator import chunkator
from django.db.models import F
from django.contrib.gis.db.models.functions import Intersection, Union
from farmlands.models import Farmland
from cities.models import City
from farmlands.models import Farmland

BATCH_SIZE = 5000

class FarmlandUnion:
	def __filter_farmland_by_city(self, polygon_obj):
		return Farmland.objects.filter(city_id=polygon_obj.city_id)

	def __get_intersected_polygons(self, polygon_obj):
		query_set_by_city = self.__filter_farmland_by_city(polygon_obj)
		return query_set_by_city.filter(geom__intersects=polygon_obj.geom).exclude(id=polygon_obj.id).all()

	def __calculate_intersection_and_union(self, polygon_obj):
		return self.__get_intersected_polygons(polygon_obj).annotate(
			intersection=Intersection(F('geom'), polygon_obj.geom), union=Union(F('geom'), polygon_obj.geom))

	def __calculate_IoU(self, polygon_obj):
		IoU = polygon_obj.intersection.area / polygon_obj.union.area
		return IoU

	def __union_polygons(self, polygon_obj, overlapped_polygon_obj):
		polygon_obj.geom = overlapped_polygon_obj.union
		polygon_obj.save()
		overlapped_polygon_obj.delete()

	def union_overlapped_farmlands(self, IoU_THRESH=None):
		for polygon_obj in chunkator(Farmland.objects.all(), BATCH_SIZE):
			# TODO: solve self intersection error(湯原)
			try:
				intersected_polygons = self.__calculate_intersection_and_union(polygon_obj)
				for overlapped_polygon in intersected_polygons:
					if IoU_THRESH is None:
						self.__union_polygons(polygon_obj, overlapped_polygon)
						continue
					IoU = self.__calculate_IoU(overlapped_polygon)
					if IoU_THRESH < IoU:
						self.__union_polygons(polygon_obj, overlapped_polygon)
			except:
				continue

def run(*args):
	farm_uni = FarmlandUnion()
	if args:
		farm_uni.union_overlapped_farmlands(float(args[0]))
	else:
		farm_uni.union_overlapped_farmlands()
