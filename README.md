# autopolygons_api
自動ポリゴンで作成されたポリゴンを提供するAPI

## seedデータ挿入

```
# --script-argsを指定すると数字に応じて結合するポリゴンのIoUの閾値が決まる。
# 指定しなければ少しでもintersectsしていれば結合される。

python manage.py runscript seeds --script-args 0.7
```
