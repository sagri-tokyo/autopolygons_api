# autopolygons_api

This is a repository for a trail of patching seperated farmland polygons across images

## Insert seed data

1. put the folder which has model prediction as shp file in data/**/.
2. put fude-polygon data in data/fude_polygon/.
3. put city kml in data/data_city_polygon/ (city boundary information)

If you create polygons other than in Japan, skip 2 and 3 steps.
Create docker container

```console
docker-compose up -d
```

Insert shape files of farmland polygons into DB
```console
docker-compose run --rm unionpolygon_app python manage.py runscript seeds
```

## Merge split polygons into one polygon in DB

Pass float number after --script-args(This number is an IoU theshold to merge)

If you don't pass that, it merges when polygons are intersected

Reference of intersection(in Japanse). http://www.pragmatica.jp/fme/references/ReferenceSpatialRelations.html

```console
docker-compose run --rm unionpolygon_app python manage.py runscript farmland_union --script-args 0.1
```

## Convert polygons in DB to shape and kml files

```console
mkdir {shp,kml} (create folders for shape file and kml file)　
docker-compose run --rm unionpolygon_app sh scripts/create_kml_from_geom.sh autopolygon_api (name of db)
```
