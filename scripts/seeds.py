import os
from django.contrib.gis.geos import Polygon, MultiPolygon
from farmlands.models import Farmland
from prefectures.models import Prefecture
from cities.models import City
from chunkator import chunkator
import xml.etree.ElementTree as ET
import glob
import re
from .layer_mappings.custom_polygon_layer_mapping import CustomPolygonLayerMapping
from django.db.models import F
from django.contrib.gis.db.models.functions import Intersection, Union, MakeValid

PREFECTURES = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

BATCH_SIZE = 1000

def insert_prefectures_to_db():
	for pref in PREFECTURES:
		pref_obj = Prefecture(name=pref)
		pref_obj.save()

def insert_cities_to_db(fude_polygon_path='data/fude_polygon/', city_polygon_kml='data_city_polygon/city_polygon.kml'):
	city_paths = glob.glob(os.path.join(os.path.dirname(__file__), fude_polygon_path, '*/*'))
	city_polygon_path = os.path.join(os.path.dirname(__file__), city_polygon_kml)

	with open(city_polygon_path, 'r', encoding="utf-8", errors='ignore') as file:
		doc = file.read()
		doc = doc.replace('\t', '').replace('\n', '')

	city_set = set()
	for city_path in sorted(city_paths):
		matched_pref = re.search(r'/\d{2}(?P<pref_name>.{2,4})（.*/', city_path)
		if matched_pref == None:
			continue
		prefecture = matched_pref.group('pref_name')
		pref_obj = Prefecture.objects.all().filter(name=prefecture).first()
		matched_city = re.search(r'\d*(?P<city_name>\D*)', os.path.basename(city_path))
		if matched_city == None:
			continue
		city = matched_city.group('city_name').replace('（', '').replace('_', '')
		if (city in city_set):
			continue
		multi_geometry = re.search(f'{city}.*?(<MultiGeometry>.+?</MultiGeometry>)', doc)
		coordinates_list = re.findall('(<coordinates>.+?</coordinates>)', multi_geometry.group())
		polygons = []
		for coordinates in coordinates_list:
			coordinates_extracted = re.findall('(\d{3}\.\d{1,}),(\d{2}\.\d{1,})', coordinates)
			coordinates_extracted = tuple((float(coordinate_extracted[0]), float(coordinate_extracted[1])) for coordinate_extracted in coordinates_extracted)
			polygons.append(Polygon(coordinates_extracted))
		city_object = City(name=city, prefecture=pref_obj, geom=MultiPolygon(polygons))
		city_object.save()
		city_set.add(city)

class FarmlandManager:
	def __calculate_intersection_union(self, polygon_obj):
		query_set_by_city = Farmland.objects.filter(city_id=polygon_obj.city_id)
		return query_set_by_city.filter(geom__intersects=polygon_obj.geom).all(
		).annotate(intersection=Intersection(F('geom'), polygon_obj.geom), union=Union(F('geom'), polygon_obj.geom))

	def __calculate_IoU(self, polygon_obj):
		IoU = polygon_obj.intersection.area / polygon_obj.union.area
		return IoU

	def insert_farmlands_to_db(self):
		farmlands_paths = glob.iglob(os.path.join(os.path.dirname(__file__), 'data/autopolygon/*.shp'))
		for farmland_path in farmlands_paths:
			farmland = CustomPolygonLayerMapping(
				model=Farmland,
				data=farmland_path,
				mapping={
					'geom': 'POLYGON'
				}
			)
			farmland.save(strict=True, verbose=True)

	def add_city_relation_to_farmlands(self):
		for polygon in chunkator(Farmland.objects.all(), BATCH_SIZE):
			city = City.objects.filter(geom__intersects=polygon.geom).first()
			polygon.city = city
			polygon.save()

	def union_overlapped_farmlands(self):
		IoU_THRESH = 0.70
		for polygon in chunkator(Farmland.objects.all(), BATCH_SIZE):
			polygon.geom = polygon.geom.buffer(0)
			try:
				overlapped_polygons = self.__calculate_intersection_union(polygon)
				for idx in range(len(overlapped_polygons)):
					IoU = self.__calculate_IoU(overlapped_polygons[idx])
					if IoU_THRESH < IoU:
						polygon.geom = polygon.geom.union(overlapped_polygons[idx].geom)
						overlapped_polygons[idx].delete()
						polygon.save()
						print(polygon.id)
			except:
				continue

def run():
	insert_prefectures_to_db()
	insert_cities_to_db()
	farm_manager = FarmlandManager()
	farm_manager.insert_farmlands_to_db()
	farm_manager.add_city_relation_to_farmlands()
	farm_manager.union_overlapped_farmlands()
