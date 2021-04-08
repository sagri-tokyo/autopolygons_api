# autopolygons_api

自動ポリゴンで作成されたポリゴンを提供するAPI

## 環境構築(Dockerを使わない場合)

```console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Gdalをインストール

## DB作成

```console
sh scripts/create_db.sh
```

## seedデータ挿入

1. data/**/にモデルの予測をshpファイルにしたフォルダを置く
2. data/fude_polygon/に筆ポリゴンデータを置く
3. data/data_city_polygon/に市町村kmlを置く(市町村の境界情報)

海外の農地でprefectureやstate、cityの境界情報が手に入らない場合は2と3はスキップ

```console
# 作成したshpファイルをまずDBに入れる
python manage.py runscript seeds
```

Dockerの場合

```console
# 作成したshpファイルをまずDBに入れる
docker-compose run --rm unionpolygon_app python manage.py runscript seeds
```

## dbに入っているfarmlandsを結合する

```console
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければintersectsしていれば結合される。
# intersectsの意味はこちらを参照。http://www.pragmatica.jp/fme/references/ReferenceSpatialRelations.html
python manage.py runscript farmland_union.py --script-args 0.1
```

Dockerの場合

```console
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければintersectsしていれば結合される。
# intersectsの意味はこちらを参照。http://www.pragmatica.jp/fme/references/ReferenceSpatialRelations.html
docker-compose run --rm unionpolygon_app python manage.py runscript farmland_union.py --script-args 0.1
```

## dbに入ってる自動ポリゴンをshpとkmlに変換

```console
sh scripts/create_kml_from_geom.sh <保存したい階層名> autopolygon_api
```

Dockerの場合

```console
docker-compose --rm unionpolygon_app sh scripts/create_kml_from_geom.sh <保存したい階層名> autopolygon_api
```

## farmland tableを初期化し、データを入れ直す

```console
# 引数はdb名
sh reset_farmland_and_insert_new_data.sh autopolygon_api
```

Dockerの場合

```console
docker-compose --rm unionpolygon_app sh reset_farmland_and_insert_new_data.sh autopolygon_api
```
