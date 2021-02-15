# autopolygons_api
自動ポリゴンで作成されたポリゴンを提供するAPI

## seedデータ挿入

- data/にモデルの予測をshpファイルにしたフォルダを置く
- data/fude_polygon/に筆ポリゴンデータを置く
- data/data_city_polygon/に市町村kmlを置く

```
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければ少しでもintersectsしていれば結合される。

python manage.py runscript seeds --script-args 0.7
```
