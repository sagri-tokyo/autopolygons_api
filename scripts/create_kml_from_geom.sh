#! /bin/bash

# postgresqlのデータをshpに変換
pgsql2shp -f shp/output.shp -u postgres -h unionpolygon_postgres $1 farmlands
# shpをkmlに変換
ogr2ogr -f KML kml/output.kml shp//output.shp
