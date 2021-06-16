#! /bin/bash

docker exec -it unionpolygon_postgres bash -c 'sh reset_farmland_table.sh autopolygon_api'
docker-compose run --rm unionpolygon_app python manage.py runscript seeds
docker-compose run --rm unionpolygon_app python manage.py runscript farmland_union --script-args $1
