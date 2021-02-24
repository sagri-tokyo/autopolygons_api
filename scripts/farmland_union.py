from chunkator import chunkator
from django.db.models import F
from django.contrib.gis.db.models.functions import Intersection, Union
from django.contrib.gis.geos import Polygon
from farmlands.models import Farmland
from cities.models import City

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
		polygon_obj.geom = polygon_obj.geom.union(overlapped_polygon_obj.geom)
		overlapped_polygon_obj.delete()
		return polygon_obj


	def union_overlapped_farmlands(self, IoU_THRESH=None):
		polygon_objs = []
		for polygon_obj in chunkator(Farmland.objects.all(), BATCH_SIZE):
			try:
				overlapped_polygons = self.__calculate_intersection_and_union(polygon_obj)
				for idx in range(len(overlapped_polygons)):
					if (IoU_THRESH):
						IoU = self.__calculate_IoU(overlapped_polygons[idx])
						if IoU_THRESH < IoU:
							polygon_obj = self.__union_polygons(polygon_obj, overlapped_polygons[idx])
					else:
						polygon_obj = self.__union_polygons(polygon_obj, overlapped_polygons[idx])
				polygon_objs.append(polygon_obj)
			except:
				continue
			if len(polygon_objs) < BATCH_SIZE: continue
			Polygon.objects.bulk_update(polygon_objs, fields=['geom'])
		Polygon.objects.bulk_update(polygon_objs, fields=['geom'])

def run(*args):
	farm_uni = FarmlandUnion()
	if args:
		farm_uni.union_overlapped_farmlands(float(args[0]))
	else:
		farm_uni.union_overlapped_farmlands()
