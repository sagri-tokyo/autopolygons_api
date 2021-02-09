import os
from django.contrib.gis.geos import Polygon, MultiPolygon
from farmlands.models import Farmland
from prefectures.models import Prefecture
from cities.models import City
from chunkator import chunkator
import glob
import re
import pdb

PREFECTURES = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', '埼玉県', '千葉県', '東京都', '神奈川県', '新潟県', '富山県', '石川県', '福井県', '山梨県', '長野県', '岐阜県', '静岡県', '愛知県', '三重県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', '鳥取県', '島根県', '岡山県', '広島県', '山口県', '徳島県', '香川県', '愛媛県', '高知県', '福岡県', '佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']

def insert_prefectures_to_db():
	for pref in PREFECTURES:
		pref_obj = Prefecture(name=pref)
		pref_obj.save()

def insert_cities_to_db(city_kml_path='data_city_polygon/city_polygon.kml'):
	city_polygon_path = os.path.join(os.path.dirname(__file__), city_kml_path)
	with open(city_polygon_path, 'r', encoding="utf-8", errors='ignore') as file:
		doc = file.read()
		doc = doc.replace('\t', '').replace('\n', '')
	city_pref_list = re.findall(r'"KEN">(?P<prefecture>.+?)<.*?"CITY_ENG">(?P<city>.+?)<', doc)
	for city_pref in city_pref_list:
		pref_obj = Prefecture.objects.all().filter(name=city_pref[0]).first()

def run():
	# insert_prefectures_to_db()
	insert_cities_to_db()
