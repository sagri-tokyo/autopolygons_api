set -e
psql -U admin admin << EOSQL
  CREATE DATABASE autopolygon_api WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'ja_JP.UTF-8' LC_CTYPE = 'ja_JP.UTF-8';
EOSQL
