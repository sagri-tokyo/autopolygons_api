set -e
psql -U admin -d $1 <<EOSQL
  DELETE FROM farmlands;
EOSQL
python manage.py sqlsequencereset farmlands | psql $1
python manage.py runscript seeds
python manage.py runscript farmland_union --script-args $2
