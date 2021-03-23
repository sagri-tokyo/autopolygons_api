# autopolygons_api
自動ポリゴンで作成されたポリゴンを提供するAPI

## 環境構築

```console
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## seedデータ挿入

- data/にモデルの予測をshpファイルにしたフォルダを置く
- data/fude_polygon/に筆ポリゴンデータを置く
- data/data_city_polygon/に市町村kmlを置く

```
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければ少しでもintersectsしていれば結合される。

python manage.py runscript seeds --script-args 0.7
```

## dbに入ってる自動ポリゴンをshpとkmlに変換

```
sh scripts/create_kml_from_geom.sh <保存したい階層名> <db名>
```

## farmland tableを初期化し、データを入れ直す
```
# 引数はdb名
sh reset_farmland_and_insert_new_data.sh autopolygon_api_development
```
