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

PREFECTURES = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

BATCH_SIZE = 5000

def insert_prefectures_to_db():
	pref_objs = []
	for pref in PREFECTURES:
		pref_objs.append(Prefecture(name=pref))
	Prefecture.objects.bulk_create(pref_objs)


def insert_cities_to_db(fude_polygon_path='data/fude_polygon/', city_polygon_kml='data_city_polygon/city_polygon.kml'):
	"""

	市の境界情報をkmlをparseし、dbに入れる関数
	Todo: 日本のkmlを前提としているため、海外の場合は書き直す必要あり(湯原)
	"""

	city_paths = glob.glob(os.path.join(os.path.dirname(__file__), fude_polygon_path, '*/*'))
	city_polygon_path = os.path.join(os.path.dirname(__file__), city_polygon_kml)

	with open(city_polygon_path, 'r', encoding="utf-8", errors='ignore') as file:
		doc = file.read()
		doc = doc.replace('\t', '').replace('\n', '')

	city_set = set()
	city_objs = []
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
		city_objs.append(City(name=city, prefecture=pref_obj, geom=MultiPolygon(polygons)))
		city_set.add(city)
	City.objects.bulk_create(city_objs)


def insert_farmlands_to_db():
	farmlands_paths = glob.iglob(os.path.join(os.path.dirname(__file__), 'data/**/*.shp'))
	for farmland_path in farmlands_paths:
		farmland = CustomPolygonLayerMapping(
			model=Farmland,
			data=farmland_path,
			mapping={
				'geom': 'POLYGON'
			}
		)
		farmland.save(strict=True, verbose=True)

def add_city_relation_to_farmlands():
	target_polygon_objs = []
	for polygon_obj in chunkator(Farmland.objects.all(), BATCH_SIZE):
		city = City.objects.filter(geom__intersects=polygon_obj.geom).first()
		polygon_obj.city = city
		target_polygon_objs.append(polygon_obj)
		if len(target_polygon_objs) < BATCH_SIZE: continue
		Farmland.objects.bulk_update(target_polygon_objs, fields=['city'])
		target_polygon_objs = []
	Farmland.objects.bulk_update(target_polygon_objs, fields=['city'])

def run():
	# insert_prefectures_to_db() # 県情報が分かる場合はこちらも実行
	# insert_cities_to_db()　 # 市情報が境界情報も含めて分かる場合はこちらも実行
	insert_farmlands_to_db()
	# add_city_relation_to_farmlands()　
