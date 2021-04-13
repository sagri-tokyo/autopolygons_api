# autopolygons_api

自動ポリゴンで作成されたポリゴンをつなぎ合わせるためのプロジェクト

## seedデータ挿入

1. data/**/にモデルの予測をshpファイルにしたフォルダを置く
2. data/fude_polygon/に筆ポリゴンデータを置く
3. data/data_city_polygon/に市町村kmlを置く(市町村の境界情報)

海外の農地でprefectureやstate、cityの境界情報が手に入らない場合は2と3はスキップ

docker container作成、起動

```console
docker-compose up -d
```

```console
# 作成したshpファイルをまずDBに入れる
docker-compose run --rm unionpolygon_app python manage.py runscript seeds
```

## dbに入っているfarmlandsを結合する

```console
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければintersectsしていれば結合される。
# intersectsの意味はこちらを参照。http://www.pragmatica.jp/fme/references/ReferenceSpatialRelations.html
docker-compose run --rm unionpolygon_app python manage.py runscript farmland_union --script-args 0.1
```

## dbに入ってる自動ポリゴンをshpとkmlに変換

```console
# ローカル
mkdir {shp,kml} (shpとkml保存用のdirsを作る)　
docker-compose run --rm unionpolygon_app sh scripts/create_kml_from_geom.sh autopolygon_api (db名)
```
