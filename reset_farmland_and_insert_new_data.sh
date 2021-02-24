set -e
psql -U admin -d $1 << EOSQL
  DELETE FROM farmlands;
EOSQL
python manage.py sqlsequencereset farmlands | psql $1
python manage.py runscript seeds
