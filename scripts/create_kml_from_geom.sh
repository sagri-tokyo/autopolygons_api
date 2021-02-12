#! /bin/bash

mkdir {../shp/"$1",../kml/"$1"}
pgsql2shp -f ../shp/"$1"/output.shp -u admin -h localhost -P admin autopolygon_api_development farmlands
ogr2ogr -f KML ../kml/"$1"/output.kml ../shp/"$1"/output.shp
